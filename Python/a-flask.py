#!/usr/bin/python
# -*- encoding: utf-8 -*-

from wsgiref.simple_server import make_server


class App:
    """ Oh My Flask """
    def __init__(self,name):
        self.__name__ = name
        self.routes = []

    def route(self,path):
        return lambda handler: self.routes.append((path,handler))

    @staticmethod
    def __bytes_conv(func):
        """ convert str to bytes for python3 incompatible """
        return lambda *args,**kwargs: map(lambda s:s.encode(),func(*args,**kwargs))
    
    def run(self,port=3000):
        @App.__bytes_conv
        def serve(env,start_response):
            for path,handle in self.routes:
                if(path == env['PATH_INFO']):
                    start_response('200 OK',[('Content-Type','text/html; charset=utf-8')])
                    return [handle()]
            start_response('404 Not Found',[('Content-Type','text/html; charset=utf-8')])
            return ['404 Not Found']
        make_server('0.0.0.0',port,serve).serve_forever()

# ---------------------------------------------------------------------------------------

app = App(__name__)

@app.route('/')
def index():
    return 'HelloWorld'

if __name__=='__main__':
    app.run()
