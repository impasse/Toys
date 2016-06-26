package main

import (
	"io/ioutil"
	"log"
	"net/http"
	"os"
	"strings"
	"time"

	"gopkg.in/redis.v3"
)

const (
	expries = 12
)

var client = redis.NewClient(&redis.Options{
	Addr:     "localhost:6379",
	Password: "",
	DB:       1,
})

var logger = log.New(os.Stdout, "INFO: ", 0)

func getImageFromRedisOrNetwork(url string) ([]byte, map[string]string) {
	result, err := client.HGetAllMap(url).Result()
	if len(result) != 0 && err != redis.Nil {
		return []byte(result["data"]), map[string]string{"Content-Type": result["type"], "X-Cached-By": "Memory"}
	}
	res, _ := http.Get(url)
	contentType := res.Header.Get("Content-Type")
	if res.StatusCode != 200 || !strings.HasPrefix(contentType, "image") || res.ContentLength == 0 {
		return nil, nil
	}
	defer res.Body.Close()
	bs, _ := ioutil.ReadAll(res.Body)
	defer putImageToRedis(url, bs, res.Header)
	return bs, map[string]string{"Content-Type": contentType, "X-Cached-By": "Network"}
}

func putImageToRedis(url string, bs []byte, head http.Header) {
	if len(bs) != 0 {
		client.Pipelined(func(pipe *redis.Pipeline) error {
			pipe.HSet(url, "data", string(bs))
			pipe.HSet(url, "type", head.Get("Content-Type"))
			pipe.Expire(url, expries*time.Hour)
			return nil
		})
	}
}

func handle(w http.ResponseWriter, r *http.Request) {
	fullURL := "http:/" + r.URL.RequestURI()
	defer func() {
		logger.Printf("%v - %v", time.Now().Format(time.UnixDate), fullURL)
		if err := recover(); err != nil {
			http.NotFound(w, r)
			logger.Printf("Error: %v", err)
		}
	}()
	bs, head := getImageFromRedisOrNetwork(fullURL)
	if bs != nil && head != nil {
		for k, v := range head {
			w.Header().Set(k, v)
		}
		w.Write(bs)
	}
}

func main() {
	http.HandleFunc("/", handle)
	panic(http.ListenAndServe(":3000", nil))
}
