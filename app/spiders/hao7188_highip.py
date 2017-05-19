# -*- coding: utf-8 -*-
import scrapy
import re
import logging
import json

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors.sgml import SgmlLinkExtractor
from scrapy.linkextractors import LinkExtractor
from scrapy.http import Request

from app.items import HighIpItem


class Hao7188HighipSpider(CrawlSpider):
    """
        hao7188.com 上的高精度ip
    """
    name = "hao7188"
    allowed_domains = ["www.hao7188.com"]
    start_urls = [
        'http://www.hao7188.com',
        'http://www.hao7188.com/ip/183.230.20.71.html',
    ]

    rules = [
        Rule(LinkExtractor(allow=("http://www\.hao7188\.com$", )), callback='parse', follow=True),
        Rule(LinkExtractor(allow=("http://www\.hao7188\.com/ip", )), callback='parse_ip_info', follow=True),
    ]

    def parse_ip_info(self, response):
        try:
            item = HighIpItem()
            item['url'] = response.url
            item['ip'] = response.url.split('/')[-1].strip('.html')
            item['loc_time'] = response.css('.so_list_left').xpath('.//li[position()=9]/text()').extract_first('').split(u"：")[-1]
            item['info'] = response.css('.so_list_left').xpath('.//li[position()>1 and position()<9]/text()').extract()
            yield item
        except Exception as e:
            logging.exception(e)


