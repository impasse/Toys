#!/usr/bin/python3
# -*- encoding: utf-8 -*-
from __future__ import unicode_literals, print_function

from abc import *
from threading import local
from wsgiref.simple_server import make_server

from jinja2 import Template as Jinja2Template
# from collections import UserDict
from typing import *
from functools import reduce, wraps
from cgi import *
import mimetypes
import re
import os
import sys
import time


# class Parameter(UserDict):
#    """ parse querystring,also support array parameter"""
#     def __init__(self, raw_query_string: str):
#         data = {}
#         if raw_query_string != "":
#             params = map(lambda kv: tuple(kv.split('=')), raw_query_string.split('&'))
#             for k, v in params:
#                 if k.endswith('[]'):
#                     if k in data:
#                         data[k].append(v)
#                     else:
#                         data[k] = [v]
#                 else:
#                     data[k] = v
#         super().__init__(data)


class Request:
    """ GET/POST as params either """
    trusted_proxy = False

    def __init__(self, env: Dict):
        self._env = env
        self._body = {}
        self._cookies = []
        self._headers = {}
        self._headers.update({k.lower()[5:]: v.lower() for k, v in env.items() if k.startswith('HTTP_')})
        self._fs = FieldStorage(environ=env, fp=env['wsgi.input'], keep_blank_values=1)
        for s in self._env.get('HTTP_COOKIE', ).split(';'):
            self._cookies.append(Cookie.parse(s.strip()))

    def __repr__(self):
        return str(self.__dict__)

    @property
    def uri(self) -> Text:
        if self.query_string == '':
            return self._env.get('PATH_INFO')
        else:
            return self._env.get('PATH_INFO') + '?' + self.query_string

    @property
    def path(self) -> Text:
        return self._env.get('PATH_INFO')

    @property
    def user_agent(self) -> Text:
        return self._env.get('HTTP_USER_AGENT', '')

    @property
    def query_string(self) -> Text:
        return self._env.get('QUERY_STRING', '')

    @property
    def scheme(self) -> Text:
        return self._env.get('SERVER_PROTOCOL')

    @property
    def method(self) -> Text:
        return self._env.get('REQUEST_METHOD')

    @property
    def cookies(self) -> List:
        return self._cookies

    def cookie(self, name, default=None) -> Optional:
        for c in self.cookies:
            if name == c.__name__:
                return c
        return default

    @property
    def ip(self) -> Text:
        if Request.trusted_proxy:
            return self._env.get('HTTP_X_FORWARDED_FOR', self._env.get('REMOTE_ADDR'))
        else:
            return self._env.get('REMOTE_ADDR')

    @property
    def params(self) -> Dict:
        return dict(self._fs)

    def param(self, name, default=None) -> Optional:
        try:
            return self._fs[name]
        except KeyError:
            return default

    @property
    def headers(self) -> List:
        return self._headers

    def header(self, name, default=None) -> Optional:
        return self._headers.get(name, default)


class Cookie:
    def __init__(self, expires=None, path=None, domain=None, http_only=False, secure=False, **kwargs):
        self._cookie_jar = {}
        if len(kwargs) == 1:
            self._cookie_jar.update(kwargs)
            self.__name__ = list(kwargs)[0]
        else:
            raise Exception('Cookie Need A Value')
        if expires is not None:
            self._cookie_jar['expires'] = expires
        if path is not None:
            self._cookie_jar['path'] = path
        if domain is not None:
            self._cookie_jar['domain'] = domain
        if http_only is not False:
            self._cookie_jar['http_only'] = '1'
        if secure is not False:
            self._cookie_jar['secure'] = '1'

    def set_expires(self, t):
        self._cookie_jar['expires'] = time.strftime('%a, %d-%b-%y %H:%M:%S GMT', t)

    def __str__(self):
        return ', '.join(["{}={}".format(k, v) for k, v in self._cookie_jar.items()])

    @property
    def value(self):
        return self._cookie_jar[self.__name__]

    def __getattr__(self, item):
        return self._cookie_jar.get(item, None)

    @staticmethod
    def parse(raw_cookie) -> Type:
        def _parse() -> Generator:
            for item in raw_cookie.split(','):
                k, v = item.strip().split('=')
                yield k, v

        return Cookie(**dict(_parse()))


class Response:
    message = {
        200: 'OK',
        301: 'Moved Permanently',
        302: 'Found',
        403: 'Forbidden',
        404: 'Not Found',
        405: 'Method Not Allowed',
        500: 'Internal Server Error'
    }

    def __init__(self, body, headers=None, code=200, cookies=[], encoding=sys.getdefaultencoding()):
        self.body = body
        self.encoding = encoding
        if headers is not None:
            self._headers = headers
        else:
            self._headers = [('Content-Type', 'text/html; charset={}'.format(encoding))]
        for c in cookies:
            self._headers.append(('Set-Cookie', str(c)))
        self.code = code

    def add_header(self, *args, **kwargs):
        for t in args:
            if isinstance(t, tuple):
                self._headers.append(t)
        self._headers.extend([(k, v) for k, v in kwargs.items()])

    def render(self, start_response) -> Iterable:
        start_response('{} {}'.format(self.code, Response.message.get(self.code, 'Unknown')), self._headers)
        return map(lambda s: s.encode(self.encoding), self.body)

    __iter__ = render


class Apply:
    def __init__(self, e, s):
        self.e = e
        self.s = s

    def __call__(self, f):
        return f(self.e, self.s)


class Middleware(metaclass=ABCMeta):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def __call__(self, env, start_response) -> Callable:
        return lambda f: f(env, start_response)


class StatcFileMiddleware(Middleware):
    def __init__(self, public_folder='./public'):
        super().__init__()
        self.public_folder = public_folder

    def __call__(self, env, start_response):
        path = os.path.join(self.public_folder, env['PATH_INFO'].lstrip('/'))
        if os.path.isfile(path):
            mime = mimetypes.guess_type(path)[0]
            start_response('200 OK', [('Content-Type', mime)])

            def openfile(next_middleware):
                with open(path) as f:
                    return f.read()

            return openfile
        else:
            return super().__call__(env, start_response)


class SessionMiddleware(Middleware):
    """ Unimplement """

    def __init__(self):
        super().__init__()

    def __call__(self, *args, **kwargs):
        super().__call__(*args, **kwargs)


class App:
    """ Oh My Flask """
    __locals = local()

    def __init__(self, name):
        self.__name__ = name
        self._routes = []
        self._middlewares = []

    def route(self, path: Text, method=('GET',)):
        if path.endswith('/*'):
            path = path[0:-1] + '.*'
        path = re.sub(r'<\w+>', '([^/]+)', path)

        @wraps(self.route)
        def _route(handle):
            self._routes.append((re.compile(path), handle, [s.upper() for s in method]))

        return _route

    def add_middleware(self, middleware):
        self._middlewares.append(middleware)

    def match(self, url) -> Optional:
        for pattern, handle, methods in self._routes:
            ans = pattern.fullmatch(url)
            if ans is None or App.get_request().method not in methods:
                continue
            else:
                return pattern, handle, ans.groups()
        return None, None, None

    def error_404(self) -> Response:
        return Response('404 Not Found', code=404)

    def error_500(self) -> Response:
        return Response('500 Server Error', code=500)

    def build_response(self, handle, params=[]):
        def render(start_response):
            resp = handle(*params)
            if isinstance(resp, Exception) or resp is None:
                return self.build_response(self.error_500)
            else:
                if isinstance(resp, str):
                    return Response([resp]).render(start_response)
                elif isinstance(resp, list):
                    return Response(resp).render(start_response)
                elif isinstance(resp, Response):
                    return resp.render(start_response)
                else:
                    raise SystemError('Unknow return type {}'.format(type(resp)))

        return render

    def serve(self, env, start_response) -> Iterable:
        try:
            App.set_request(Request(env))

            def this(env, start_response):
                route, handle, params = self.match(env['PATH_INFO'])
                if route is None:
                    return self.build_response(self.error_404)(start_response)
                else:
                    return self.build_response(handle, params)(start_response)

            return reduce(lambda a, b: a(b), self._middlewares, Apply(env, start_response))(this)
        except Exception as e:
            return Response('Exception: {}'.format(repr(e)), code=500).render(start_response)

    @staticmethod
    def get_request() -> Request:
        return App.__locals.request

    @staticmethod
    def set_request(val):
        App.__locals.request = val

    __call__ = serve

    def run(self, port=3000, host='0.0.0.0'):
        make_server(host, port, self.serve).serve_forever()


class Proxy:
    def __init__(self, target):
        self._target = target

    def __getitem__(self, item):
        return getattr(self._target(), item)

    __getattr__ = __getitem__


class Template:
    def __init__(self, folder='./templates/', engine='jinja2'):
        self.engine = 'render_' + engine
        self.folder = folder

    def render_jinja2(self, filename, **kwargs) -> Response:
        fullname = os.path.join(self.folder, filename)
        if os.path.isfile(fullname):
            with open(fullname) as f:
                return Response(Jinja2Template(f.read()).stream(**kwargs))
        else:
            raise Exception('Template {} Not Exists', format(filename))

    def __call__(self, filename, **kwargs) -> Response:
        if hasattr(self, self.engine):
            return getattr(self, self.engine)(filename, request=App.get_request(), **kwargs)
        else:
            raise Exception('None Template Engine Could Be Used')


render_template = Template()
request = Proxy(App.get_request)
redirect_to = lambda path: Response('302 Temporarily Move', headers=[('Location', path)], code=302)

# Example
# ---------------------------------------------------------------------------------------

app = App(__name__)


@app.route('/')
def index():
    count = 1
    if request.cookie('count', None) is not None:
        count = int(request.cookie('count').value) + 1
    return Response("""
    <html>
    <head>
    <title>My Flask</title>
    </head>
    <body>
        <h1>Welcome</h1>
        <ul>
            <li>You are requesting {}</li>
            <li>Your IP is: {}</li>
            <li>This is {} times that you visited here</li>
            <li>Your User-Agent is: {}</li>
            <li>Your Parameters is: {}</li>
        </ul>
        <form method="POST" enctype="multipart/form-data" action="/param">
        <p>
            <input type="text" name="field1"/>
        </p>
        <p>
            <input type="text" name="field2"/>
        </p>
        <p>
            <input type="file" name="upload" />
        </p>
        <p>
            <input type="submit" value="submit"/>
        <p>
        </form>
    </body>
    </html>
    """.format(request.uri, request.ip, count, request.user_agent, request.params), cookies=[Cookie(count=count)])


@app.route('/back')
def back_home():
    return redirect_to('/')


@app.route('/<param>', method=['POST', 'GET'])
def index_post(param):
    return render_template('index.html', title='My Flask', param=param)


if __name__ == '__main__':
    app.add_middleware(StatcFileMiddleware())
    app.run()
