var http = require('http');
var spawn = require('child_process').spawn;

http.createServer(function (req, res) {
    spawn('ping', ['-t', 'zyy.cat']).stdout.pipe(res);
}).listen(3000);
