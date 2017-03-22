# coding=utf-8
# author=zhtsh

import logging
import scrapy
import scrapy_splash
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from scrapy_splash_test.items import ScrapySplashTestItem

class ScrapySplashSpider(CrawlSpider):

    name = 'scrapy_splash_crawler'
    enable_proxy = False
    custom_settings = {
        'SPLASH_URL' : 'http://192.168.1.125:8050/',
        'SPIDER_MIDDLEWARES' : {
            'scrapy_splash.SplashDeduplicateArgsMiddleware': 100,
        },
        'DOWNLOADER_MIDDLEWARES' : {
            'scrapy_splash.SplashCookiesMiddleware': 723,
            'scrapy_splash.SplashMiddleware': 725,
            'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
        },

        'DUPEFILTER_CLASS' : 'scrapy_splash.SplashAwareDupeFilter',

        'HTTPCACHE_STORAGE' : 'scrapy_splash.SplashAwareFSCacheStorage'
    }

    def start_requests(self):
        url = 'http://www.inveno.cn/'
        yield scrapy_splash.SplashRequest(url, self.parse_result,
                                          args={
                                              # optional; parameters passed to Splash HTTP API
                                              'wait': 0.5,

                                              # 'url' is prefilled from request url
                                              # 'http_method' is set to 'POST' for POST requests
                                              # 'body' is set to request body for POST requests
                                          },
                                          splash_url='http://192.168.1.125:8050/',  # optional; overrides SPLASH_URL
                                          slot_policy=scrapy_splash.SlotPolicy.PER_DOMAIN,  # optional
                                    )

    def parse_result(self, response):
        logging.info(response.url)
        contact_us_link = response.xpath("//ul[@class='footerul']/li[5]/a/@href").extract()
        if contact_us_link:
            item = ScrapySplashTestItem()
            item['url'] = contact_us_link[0]
            yield item