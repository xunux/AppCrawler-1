# -*- coding: utf-8 -*-
import scrapy

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.linkextractors import LinkExtractor
from app.items import AppItem
import json


class ZdicSpider(CrawlSpider):
    name = "zdic"
    allowed_domains = ["www.zdic.net"]
    start_urls = (
        'http://www.zdic.net/z/1a/yy/6211.htm',
        'http://www.zdic.net/z/14/yy/4E00.htm',
        'http://www.zdic.net/z/15/js/4E8C.htm',
        'http://www.zdic.net/z/14/yy/4E09.htm',
        'http://www.zdic.net/z/29/yy/9E2D.htm',
        'http://www.zdic.net/sousuo/?q=客'
    )
    rules = [
        Rule(LinkExtractor(allow=("http://www.zdic.net/z/\w+/yy/\w+.htm", )),
             callback='parse_dic', follow=True),
        Rule(LinkExtractor(allow=("http://www.zdic.net/z/\w+/js/\w+.htm", )),
             callback='parse', follow=True),
    ]

    def parse_dic(self, response):
        zi = {}
        zi['url'] = response.url
        zi['unicode'] = zi['url'].split('/')[-1].split('.')[0]
        # zi['name'] = unichr(int(zi['unicode'], 16))
        zi['name'] = response.css('#ziip::text').extract_first().strip()[1]
        zys = response.css('#zy > .tab-page > p').xpath('.//text()').extract()
        if zys:
            for l in zys:
                if l.startswith(u'◎ 客家话'):
                    zi['hakka'] = l
                elif l.startswith(u'◎ 粤语'):
                    zi['yueyu'] = l
                elif l.startswith(u'◎ 潮州话'):
                    zi['hoklau'] = l
                else:
                    zi['other'] += l
            # print(json.dumps(zi, ensure_ascii=False, indent=4))
            yield zi
