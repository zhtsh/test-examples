# coding=utf-8
# author=zhtsh

import scrapy
import re, time
from datetime import datetime
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from scrapy_proxy.items import ScrapyProxyItem

class ScrapyProxySpider(CrawlSpider):

    name = 'scrapy_proxy_crawler'
    allowed_domains = ['google.com']
    start_urls = ['https://play.google.com/store/apps']
    enable_proxy = True

    def parse_start_url(self, response):
        items = response.xpath("//div[@class='details']/a[2]/text()").extract()
        for name in items:
            name = name.strip()
            if name:
                item = ScrapyProxyItem()
                item['name'] = name
                yield item