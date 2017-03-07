#!/usr/bin/python
# coding=utf8

# US region middleware class
class USProxyMiddleware(object):


    def process_request(self, request, spider):
        # Set the proxy server
        request.meta['proxy'] = "http://54.193.51.137:3120"

# SG region middleware class
class SGProxyMiddleware(object):


    def process_request(self, request, spider):
        # Set the proxy server
        request.meta['proxy'] = "http://54.169.250.252:3120"

# JP region middleware class
class JPProxyMiddleware(object):


    def process_request(self, request, spider):
        # Set the proxy server
        request.meta['proxy'] = "http://13.112.194.185:3120"