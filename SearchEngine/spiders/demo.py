# -*- coding: utf-8 -*-
import scrapy
import uuid
import json
import pytz
import datetime
from scrapy.utils.log import logger
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from SearchEngine.items import SearchEngineItem


class DemoSpider(scrapy.Spider):
    name = 'demo'
    allowed_domains = []
    start_urls = []
    custom_settings = {
        'BOT_NAME': 'SearchEngine',
        'LOG_LEVEL': 'INFO',
        'RETRY_ENABLED': False,
        'DOWNLOADER_MIDDLEWARES': {
            # 'SearchEngine.middlewares.ProxyMiddleware': 100,
        },
        'ITEM_PIPELINES': {
            'SearchEngine.pipelines.MysqlTwistedPipeline': 100,
        },
    }

    def __init__(self, conf, *args, **kwargs):
        conf = json.loads(conf)
        logger.info(conf)
        self.allowed_domains.extend(conf['allowed_domains'])
        self.start_urls.extend(conf['start_urls'])
        # self.custom_settings.update(conf['custom_settings'])
        super(DemoSpider, self).__init__(*args, **kwargs)


    def parse(self, response):
        try:
            # head
            url = response.url
            url_parse = urlparse(url)
            domain = url_parse.hostname
            html = BeautifulSoup(response.body, 'lxml')
            head = html.find('head')
            title = head.find('title').get_text()
            try:
                keywords = head.find('meta', attrs={"name": "keywords"})['value']
            except Exception as e:
                keywords = ""
            try:
                description = head.find('meta', attrs={"name": "description"})['value']
            except Exception as e:
                description = ""
            item = SearchEngineItem()
            item['uuid'] = str(uuid.uuid5(uuid.NAMESPACE_URL, url))
            item['url'] = url
            item['domain'] = domain
            item['title'] = title
            item['keywords'] = keywords
            item['description'] = description
            item['verified'] = 1
            item['update'] = datetime.datetime.now(pytz.utc)
            yield item
            logger.info('New item scrapped: <[uuid]: %s, [url]: %s, [domain]: %s, [title]: %s>', item['uuid'], item['url'], item['domain'], item['title'])
            # body
            body = html.find('body')
            aTags = body.find_all('a')
            for aTag in aTags:
                try:
                    # if self.is_legal_url(aTag['href']):
                    url = response.urljoin(aTag['href'])
                    yield scrapy.Request(url=url, callback=self.parse, errback=self.errback)
                except Exception as e:
                    logger.error('Failed to yield a new request: <[reason]: %s>', e)
        except Exception as e:
            logger.error('Failed to parse a response: <[reason]: %s>', e)

    def is_legal_url(self, href):
        url_parse = urlparse(href)
        if url_parse.scheme == 'http' or url_parse.scheme == 'https':
            if url_parse.hostname:
                return True
            else:
                return False
        else:
            return False

    def errback(self, failure):
        logger.error('Failed to get response: <[reason]: %s>', repr(failure))
