#!/usr/bin/python3
# -*- encoding:utf-8 -*-
from __future__ import unicode_literals
from wsgiref.simple_server import make_server

def app(env,start_response):
	start_response('200 OK',[('Content-Type', 'text/plain; charset=utf-8')])
	return ["\r\n".join(["{}:{}".format(k,v) for k,v in env.items()]).encode('utf-8')]
	
make_server('0.0.0.0',8080,app).serve_forever()
