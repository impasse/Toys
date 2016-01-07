/*
spider for shyling.com
license GPL V2
@author shyling
*/

var request = require('request');
var cheerio = require('cheerio');

/*
util
*/
function get(url, callback) {
    request(url, function (err, res, data) {
        if (!err && res.statusCode == 200) {
            callback(cheerio.load(data));
        }
    });
}

/*
从文章列表开始爬
*/
function fetchPost(page_url) {
    get(page_url, $=> {
        $('.article-title').each(function () {
            get($(this).attr('href'), $=> {
                console.log("标题:",
                    $('.article-title').text(),
                    "\n内容:",
                    $('.article-entry').text(),
                    '\n--------------------------------\n'
                    );
            });
        });
    });
}

/*
偷懒:直接就看出来有多少页了嘛
*/
for (var i = 1; i < 7; i++) {
    fetchPost(`https://shyling.com/page/${i}/`)
}