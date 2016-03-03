#!/usr/bin/python2
# -*- encoding=utf-8 -*-
from __future__ import unicode_literals
from meinheld import server
from flask import request, Flask, make_response, Response
import json

app = Flask(__name__)

now = [
    {'id': "云南", 'name': 4310002},
    {'id': '甘肃', 'name': 4042485},
    {'id': '贵州', 'name': 3937947},
    {'id': '陕西', 'name': 3247416},
    {'id': '河南', 'name': 3221529},
    {'id': '四川', 'name': 3171342},
    {'id': '河北', 'name': 3170488},
    {'id': '内蒙古', 'name': 3089376},
    {'id': '山东', 'name': 3072568},
    {'id': '新疆', 'name': 2937356},
    {'id': '湖北', 'name': 2573506},
    {'id': '安徽', 'name': 2548168},
    {'id': '湖南', 'name': 2298515},
    {'id': '广西', 'name': 2210454},
    {'id': '江西', 'name': 1592919},
    {'id': '重庆', 'name': 1523792},
    {'id': '黑龙江', 'name': 1428478},
    {'id': '吉林', 'name': 1328311},
    {'id': '辽宁', 'name': 1258486},
    {'id': '山西', 'name': 1227603},
    {'id': '宁夏', 'name': 1126275},
    {'id': '广东', 'name': 1104871},
    {'id': '福建', 'name': 1042996},
    {'id': '江苏', 'name': 954904},
    {'id': '浙江', 'name': 786494},
    {'id': '海南', 'name': 770614},
    {'id': '青海', 'name': 683075},
    {'id': '上海', 'name': 189489},
    {'id': '天津', 'name': 94778},
    {'id': '北京', 'name': 63773}
]

all = [
    {'id': '云南', 'name': 3478},
    {'id': '甘肃', 'name': 912},
    {'id': '贵州', 'name': 3141},
    {'id': '陕西', 'name': 756},
    {'id': '河南', 'name': 697},
    {'id': '四川', 'name': 830},
    {'id': '河北', 'name': 994},
    {'id': '内蒙古', 'name': 780},
    {'id': '山东', 'name': 495},
    {'id': '新疆', 'name': 353},
    {'id': '湖北', 'name': 1416},
    {'id': '安徽', 'name': 384},
    {'id': '湖南', 'name': 1708},
    {'id': '广西', 'name': 1691},
    {'id': '江西', 'name': 840},
    {'id': '重庆', 'name': 1103},
    {'id': '黑龙江', 'name': 409},
    {'id': '吉林', 'name': 489},
    {'id': '辽宁', 'name': 530},
    {'id': '山西', 'name': 1199},
    {'id': '宁夏', 'name': 425},
    {'id': '广东', 'name': 510},
    {'id': '福建', 'name': 515},
    {'id': '江苏', 'name': 253},
    {'id': '浙江', 'name': 176},
    {'id': '海南', 'name': 428},
    {'id': '青海', 'name': 253},
    {'id': '上海', 'name': 27},
    {'id': '天津', 'name': 25},
    {'id': '北京', 'name': 43}
]


def jsonp(func):
    """decorator for jsonp request"""

    def decorator(*args, **kwargs):
        callback = request.args.get('callback', False)
        content = func(*args, **kwargs)
        if isinstance(content, Response):
            return content
        if callback:
            content = Response("%s(%s)" % (callback, json.dumps(content, ensure_ascii=False)),
                               mimetype='application/javascript')
        else:
            content = Response(
                json.dumps(content,ensure_ascii=False), mimetype='application/json')
        return content

    return decorator


@app.route('/api/<file>')
@jsonp
def api(file):
    if file == 'all':
        return all
    elif file == 'now':
        return now
    else:
        return make_response('404 Not Found', 404)


if __name__ == '__main__':
    server.set_access_logger(None)
    server.set_error_logger(None)
    server.listen(('127.0.0.1',3001))
    server.run(app)
