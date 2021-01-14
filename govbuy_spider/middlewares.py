# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html
import random
from govbuy_spider.settings import IPPOOL
import scrapy
from scrapy import signals
import redis

from utils.tools import DealBidTools
from govbuy_spider.settings import REDIS_HOST, REDIS_PORT, REDIS_DB
import hashlib


class GovbuySpiderSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    def __init__(self):
        self.conRedis = redis.StrictRedis(
            host=REDIS_HOST,
            port=REDIS_PORT,
            db=REDIS_DB,
            # password = REDIS_PWD
        )

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.

        for i in result:

            if isinstance(i, scrapy.Request):
                url = DealBidTools.md5(i.url)

                if self.conRedis.exists('url:%s' % url):
                    print("IgnoreRequest : %s" % i)
                    pass
                else:
                    yield i
            else:
                yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class GovbuySpiderDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod

    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class MyproxiesSpiderMiddleware(object):


    def __init__(self, ip):
        self.ip = ip

    @classmethod
    def from_crawler(cls, crawler):
        return cls(ip=crawler.settings.get('PROXIES'))

    def process_request(self, request, spider):
        ip = "http://192.168.2.74:8118"
        # ip = "http://127.0.0.1:8118"
        # ip = "https://192.168.2.43:1088"
        request.meta['proxy'] = ip
        print(request.meta['proxy'])


