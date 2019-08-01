# -*- coding: utf-8 -*-
import scrapy


class SearchEngineItem(scrapy.Item):
    uuid = scrapy.Field()
    domain = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()
    keywords = scrapy.Field()
    description = scrapy.Field()
    verified = scrapy.Field()
    update = scrapy.Field()

    def get_insert_sql(self):
        insert_sql = """REPLACE INTO item (`uuid`,`url`,`domain`,`title`,`keywords`,`description`,`verified`,`update`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s);"""
        params = (self['uuid'], self['url'], self['domain'], self['title'], self['keywords'], self['description'], self['verified'], self['update'])
        return insert_sql, params
