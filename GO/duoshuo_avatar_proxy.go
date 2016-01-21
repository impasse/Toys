package main

import (
	"fmt"
	"io/ioutil"
	"net/http"
	"time"
)

const (
	prefix  = "http:/"
	timeout = 10
)

func proxy(resw http.ResponseWriter, req *http.Request) {
	url := prefix + req.URL.RequestURI()
	fmt.Printf("Request From %s URL: %s \n", req.RemoteAddr, url)
	
	client := &http.Client{Timeout: time.Second * timeout}
	requestRes, err := client.Get(url)
	
	if err == nil && requestRes.StatusCode == 200 {
		header := resw.Header()
		for key, values := range requestRes.Header {
			if len(values) == 1 {
				header.Add(key, values[0])
			} else {
				for _, value := range values {
					header.Add(key, value)
				}
			}
		}
		data, _ := ioutil.ReadAll(requestRes.Body)
		resw.Write(data)
	} else {
		fmt.Println(err)
		fmt.Fprintln(resw, "FILE NOT FOUND")
	}
}

func main() {
	http.HandleFunc("/", proxy)
	err := http.ListenAndServe("127.0.0.1:3000", nil)
	if err != nil {
		fmt.Println("Server Started")
	}
}
