# -*- coding: utf-8 -*-
import scrapy
import re

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.linkextractors import LinkExtractor
from app.items import CoolapkItem

category_dict = {
    "apk": u"应用",
    "game": u"游戏",
}

class CoolpakSpider(CrawlSpider):
    """
        酷安应用爬虫
    """
    name = "coolapk"
    allowed_domains = ["coolapk.com"]
    start_urls = [
        'http://www.coolapk.com/apk/',
        'http://www.coolapk.com/game/',
    ]
    rules = [
       # Rule(LinkExtractor(allow=("http://apk\.hiapk\.com/appinfo/", )), callback='parse_app',follow=True),
       #  Rule(LinkExtractor(allow=("http://apk\.hiapk\.com/apps?sort=\d+&pi=\d+", )), callback='parse',follow=True),
       #  Rule(LinkExtractor(allow=("http://apk\.hiapk\.com/games.*?sort=\d+&pi=\d+", )), callback='parse',follow=True),
        Rule(LinkExtractor(allow=("http://www\.coolapk\.com/apk/\?p=\d+", )), callback='parse_app',follow=True),
        Rule(LinkExtractor(allow=("http://www\.coolapk\.com/game/\?p=\d+", )), callback='parse_app',follow=True),
    ]

    # def start_requests(self):
    #     for base_url in self.start_urls:
    #         for ra in range(1,6):
    #             for i in [5, 8, 9]:
    #                     url = base_url + "?sort=" + str(i) + "&ra=" + str(ra)
    #                     yield self.make_requests_from_url(url)

    def parse_app(self, response):
        selector_list = response.css('div.row >div:nth-child(1) .panel ul.media-list li')
        for sel in selector_list:
            try:
                item = CoolapkItem()
                item['url'] = response.url
                item['name'] = sel.css('.media-body a').xpath('text()').extract_first('')
                app_url = sel.css('.media-body a').xpath('@href').extract_first('')
                item['package'] = app_url.split('/')[2]
                item['apk_url'] = 'http://www.coolapk.com' + app_url
                item['icon'] = sel.xpath('.//a/img/@src').extract_first('')
                item['version'] = sel.css('.media-info .apk-version').xpath('text()').extract_first('')
                item['category'] = category_dict.get(app_url.split('/')[1])
                item['editor_comment'] = sel.css('.media-intro').xpath('text()').extract_first('').strip('')
                info = sel.css('.media-info span:nth-child(2)').xpath('text()').extract_first('')
                item['apk_size'] = info.split(u'，')[0]
                item['download_num'] = info.split(u'，')[1].replace(u'\xa0', '').rtrip(u"次下载")
                item['star_num'] = sel.css('.media-info span:nth-child(3)').xpath('text()').extract_first('')
                yield item
            except Exception as e:
                print item
                raise e


  
