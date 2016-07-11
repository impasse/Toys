const fs = require('fs')
const co = require('co')
const axios = require('axios')
const cheerio = require('cheerio')
const sleep = require('es6-sleep').promise;

const client = axios.create({baseURL: 'http://v2ex.com',headers: {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36'}})
const out_file = fs.createWriteStream('posts.txt')

function * post_info (name, url) {
  let $ = cheerio.load((yield client.get(url)).data)
  out_file.write(`${$('h1').text()}\r\n-------------------------------------\r\n`)
  out_file.write(`${$('.topic_content').text()}\r\n\r\n`)
  yield sleep(1000)
}

co(function * () {
  let $ = cheerio.load((yield client.get('/?tab=all')).data)
  let posts = $('.item span.item_title > a')
  for (let i = 0;i < posts.length;++i) {
    yield post_info($(posts[i]).text(), $(posts[i]).attr('href'))
  }
  out_file.end()
}).catch(console.error)
