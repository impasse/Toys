package main

import (
	"fmt"
	"io"
	"net/http"
	"net/url"
	"os"
	"sync"
	"time"
)

const (
	prefix  = "http:/"
	timeout = 10
)

var client *http.Client
var bufferPol *sync.Pool

func copyBuffer(dst io.Writer, src io.Reader) (written int64, err error) {
	buf := bufferPol.Get().([]byte)
	defer bufferPol.Put(buf)
	return io.CopyBuffer(dst, src, buf)
}

func proxyHandle(resw http.ResponseWriter, req *http.Request) {
	defer func() {
		if rec := recover(); rec != nil {
			fmt.Fprintf(os.Stderr, "Error: %v", rec)
			http.NotFound(resw, req)
		}
	}()
	reqURL, err := url.Parse(prefix + req.URL.RequestURI())
	if err != nil {
		panic(err)
	}
	fmt.Printf("%v - %v | %v | %v \n", req.Method, reqURL, req.RemoteAddr, time.Now())

	reqHeader := http.Header{
		"Accept":          {"image/*"},
		"Accept-Encoding": {"gzip,deflate"},
		"Host":            {reqURL.Host},
		"Referer":         {reqURL.String()},
		"User-Agent":      {req.Header.Get("User-Agent")}}
	request := &http.Request{
		Method: "GET",
		Header: reqHeader,
		URL:    reqURL}
	requestRes, err := client.Do(request)
	if err != nil {
		panic(err)
	}
	if requestRes.StatusCode == 200 {
		header := resw.Header()
		for key, values := range requestRes.Header {
			for _, value := range values {
				header.Add(key, value)
			}
		}
		defer requestRes.Body.Close()
		copyBuffer(resw, requestRes.Body)
	} else {
		panic(requestRes.StatusCode)
	}
}

func main() {
	client = &http.Client{Timeout: time.Second * timeout}
	bufferPol = &sync.Pool{
		New: func() interface{} {
			return make([]byte, 1024*64) //64kb的buffer
		}}

	http.HandleFunc("/", proxyHandle)
	panic(http.ListenAndServe("127.0.0.1:3000", nil))
}