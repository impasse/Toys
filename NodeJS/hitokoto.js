/*
* 一言API的NodeJS代理
* Author:shyling
* Date: 1451927268453
* License: GPL V2
*/

var http = require('http');

/*
解析jsonp格式
<p>不在服务端使用eval</p>
*/
function parseHitokoto(str) {
    var pattern = /hitokoto\((\{.+\})\)/;
    try {
        var obj = JSON.parse(str.match(pattern)[1]);
        console.log(obj);
        return '<script>document.write("' + obj.hitokoto + '");</script>';
    } catch (e) {
        console.error(e);
    }
}


var server = http.createServer(function (req, res) {
    http.get('http://api.hitokoto.us/rand?encode=jsc&fun=hitokoto', function (conn) {
        if (conn.statusCode != 200) {
            conn.throw(404);
        }
        var buffers = []
        conn.on('data', function (chunk) {
            buffers.push(chunk);
        })
        conn.on('end', function () {
            var body = Buffer.concat(buffers).toString();
            res.writeHead(200, {
                'Content-Type': 'application/javascript'
            })
            res.end(parseHitokoto(body));
        })
    });
});

server.listen(3000);