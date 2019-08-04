# -*- coding: utf-8 -*-


class ProxyMiddleware(object):
    def process_request(self, request, spider):
        if request.url.startswith('https'):
            request.meta['proxy'] = "https://root:yvette0218@127.0.0.1:1080"
        if request.url.startswith('http'):
            request.meta['proxy'] = "http://root:yvette0218@127.0.0.1:1080"
