#!/usr/bin/python
# coding=utf8
# author=david

import json
import random
import time
from datetime import date
import tornado.escape
import tornado.ioloop
import tornado.web
import tornado.gen
import tornado.httpclient

class VersionHandler(tornado.web.RequestHandler):
    def get(self):
        response = {
            'version' : '3.5.1',
            'last_build' : date.today().isoformat()
        }
        self.write(response)
        # self.write("Version: 3.5.1. Last build: " + date.today().isoformat())
        # self.set_header("Content-Type", "text/plain")

class VersionAsyncHandler(tornado.web.RequestHandler):
    @tornado.gen.coroutine
    def get(self):
        print 'Receiving request from client'
        print int(time.time())
        seed = random.randint(1, 10)
        print seed
        status = yield tornado.gen.Task(self.get_response, seed)
        if status:
            print(self.response)
            self.write(self.response)
        else:
            response = {
                'version': 'unknown',
                'last_build': date.today().isoformat()
            }
            self.write(response)
        self.finish()

    @tornado.gen.coroutine
    def get_response(self, seed):
        time.sleep(0.2)
        self.response = {
            'seed': seed,
            'version': '3.5.1',
            'last_build': int(time.time())
        }
        return True

class GetGameByIdHandler(tornado.web.RequestHandler):
    def initialize(self, common_string):
        self.common_string = common_string

    def get(self, id):
        response = {
            'id' : int(id),
            'name' : 'Crazy Game',
            'release_date' : date.today().isoformat(),
            'common_string' : self.common_string
        }
        self.write(response)

class GetFullPageAsyncHandler(tornado.web.RequestHandler):
    @tornado.gen.coroutine
    def get(self):
        http_client = tornado.httpclient.AsyncHTTPClient()
        http_response = yield http_client.fetch("http://www.drdobbs.com/web-development")
        response = http_response.body.decode().replace(
            "Most Recent Premium Content", "Most Recent Content")
        self.write(response)
        self.set_header("Content-Type", "text/html")

# class GetFullPageAsyncHandler(tornado.web.RequestHandler):
#     @tornado.web.asynchronous
#     def get(self):
#         http_client = tornado.httpclient.AsyncHTTPClient()
#         http_client.fetch("http://www.drdobbs.com/web-development", callback=self.on_fetch)
#
#     def on_fetch(self, http_response):
#         if http_response.error:
#             raise tornado.web.HTTPError(500)
#         response = http_response.body.decode().replace(
#             "Most Recent Premium Content", "Most Recent Content")
#         self.write(response)
#         self.set_header("Content-Type", "text/html")
#         self.finish()

class TestHandlerAsync(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def get(self):
        print('a')
        client = tornado.httpclient.AsyncHTTPClient()
        client.fetch("http://www.weather.com.cn/data/sk/101010100.html" ,
                callback=self.on_response)
        print('b')

    def on_response(self, response):
        try:
            body = json.loads(response.body)
            result_count = len(body['weatherinfo'])
            self.write(body['weatherinfo']['city'])
        except:
            self.write('request failed')
        print('c')
        self.finish()

class TestHandlerGen(tornado.web.RequestHandler):
    @tornado.gen.coroutine
    def get(self):
        print 'Receiving request from client'
        client = tornado.httpclient.AsyncHTTPClient()
        response = yield tornado.gen.Task(client.fetch,
                "http://www.weather.com.cn/data/sk/101010100.html" )
        body = json.loads(response.body)
        print body
        result_count = len(body['weatherinfo'])
        self.write(body['weatherinfo']['city'])
        self.finish()

class TestHandlerSync(tornado.web.RequestHandler):
    def get(self):
        print('a')
        client = tornado.httpclient.HTTPClient()
        response = client.fetch("http://www.weather.com.cn/data/sk/101010100.html" )
        print('b')
        try:
            body = json.loads(response.body)
            result_count = len(body['weatherinfo'])
            self.write(body['weatherinfo']['city'])
        except:
            self.write('request failed')
        print('c')
        self.finish()

class SyncHandler(tornado.web.RequestHandler):
    def get(self):
        response = json.load(open('response.json', 'rb'))
        self.write(response)
        self.set_header("Content-Type", "text/json")

class AsyncHandler(tornado.web.RequestHandler):
    @tornado.gen.coroutine
    def get(self):
        response = yield self.get_response()
        self.write(response)
        self.finish()

    @tornado.gen.coroutine
    def get_response(self):
        response = json.load(open('response.json', 'rb'))
        return response

def make_app():
    return tornado.web.Application([
        (r"/getfullpage", GetFullPageAsyncHandler),
        (r"/getgamebyid/([0-9]+)", GetGameByIdHandler, {'common_string' : 'Hello, world'}),
        (r"/version", VersionHandler),
        (r"/versionasync", VersionAsyncHandler),
        (r"/testasync", TestHandlerAsync),
        (r"/testgen", TestHandlerGen),
        (r"/testsync", TestHandlerSync),
        (r"/sync", SyncHandler),
        (r"/async", AsyncHandler),
    ])

if __name__ == '__main__':
    import logging
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()