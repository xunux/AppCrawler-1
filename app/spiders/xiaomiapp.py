# -*- coding: utf-8 -*-
import scrapy
import re
import logging
import json

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors.sgml import SgmlLinkExtractor
from scrapy.linkextractors import LinkExtractor
from scrapy.http import Request

from app.items import XiaomiAppItem

top_category_dict = {

}

category_dict = {

}

class XiaomiAppSpider(CrawlSpider):
    """
        酷安应用爬虫
    """
    name = "xiaomi_app"
    allowed_domains = ["app.mi.com"]
    start_urls = [
        'http://app.mi.com',
    ]

    rules = [
       # Rule(LinkExtractor(allow=("http://apk\.hiapk\.com/appinfo/", )), callback='parse_app',follow=True),
       #  Rule(LinkExtractor(allow=("http://apk\.hiapk\.com/apps?sort=\d+&pi=\d+", )), callback='parse',follow=True),
       #  Rule(LinkExtractor(allow=("http://apk\.hiapk\.com/games.*?sort=\d+&pi=\d+", )), callback='parse',follow=True),
        Rule(LinkExtractor(allow=("http://app\.mi\.com$", )), callback='parse_category', follow=True),
        Rule(LinkExtractor(allow=("http://app\.mi\.com/.+", )), callback='parse', follow=True),
        # Rule(LinkExtractor(allow=("http://app\.mi\.com/category/", )), callback='parse', follow=True),
        Rule(LinkExtractor(allow=("http://app\.mi\.com/details\?id=([a-zA-Z0-9]+\.)+[a-zA-Z0-9]+", )), callback='parse_app_info', follow=True),
    ]

    # http://app.mi.com/categotyAllListApi?page=0&categoryId=14&pageSize=2000
    def start_requests(self):
        yield Request(self.start_urls[0], self.parse_category)

    def parse_category(self, response):
        app_selector_list = response.css('div.sidebar div:nth-child(2) ul li')
        for app_sel in app_selector_list:
            c_name = app_sel.xpath('.//text()').extract_first('')
            c_id = app_sel.xpath('.//@href').extract_first('').split('/')[-1]
            top_category_dict[c_name] = u'应用'
            category_dict[c_name] = c_id

        game_selector_list = response.css('div.sidebar div:nth-child(3) ul li')
        for game_sel in game_selector_list:
            c_name = game_sel.xpath('.//text()').extract_first('')
            c_id = game_sel.xpath('.//@href').extract_first('').split('/')[-1]
            top_category_dict[c_name] = u'游戏'
            category_dict[c_name] = c_id

        for c_id in category_dict.itervalues():
            url = 'http://app.mi.com/categotyAllListApi?page=0&categoryId=%s&pageSize=2000' % (c_id,)
            yield Request(url, callback=self.parse_app)

    def parse_app(self, response):
        app_data = json.loads(response.body)["data"]
        for row in app_data:
            item = XiaomiAppItem()
            item['appid'] = row['appId']
            item['name'] = row['displayName']
            item['icon'] = row['icon']
            item['category'] = row['level1CategoryName']
            item['top_category'] = top_category_dict.get(row['level1CategoryName'])
            item['package'] = row['packageName']
            # yield item
            yield Request('http://app.mi.com/details?id=' + row['packageName'], self.parse_app_info)

    def parse_app_info(self, response):
        try:
            item = XiaomiAppItem()
            item['url'] = response.url
            item['name'] = response.css('.intro-titles').xpath('.//h3/text()').extract_first()
            item['company'] = response.css('.intro-titles').xpath('.//p[1]/text()').extract_first()
            item['info'] = " ".join(response.css('.details ul li').xpath('.//text()').extract()).strip()
            item['introduce'] = ''.join(response.css('.app-text .pslide:nth-child(2)').xpath('.//text()').extract())
            item['imprint'] = ''.join(response.css('.app-text .pslide:nth-child(4)').xpath('.//text()').extract())
            item['category'] = response.css('.bread-crumb ul li:nth-child(2) a').xpath('text()').extract_first('')
            item['top_category'] = top_category_dict.get(item['category'])
            item['apk_url'] = 'http://app.mi.com' + response.css('.app-info-down a').xpath('.//@href').extract_first()
            item['icon'] = response.css('.app-info > img').xpath('@src').extract_first('')

            detail_info = response.css('.details ul li').xpath('.//text()').extract()
            item['apk_size'] = detail_info[1]
            item['version'] = detail_info[3]
            item['version'] = detail_info[5]
            item['package'] = detail_info[7]
            item['appid'] = detail_info[9]
            item['star_num'] = response.css('.intro-titles .star1-empty div').xpath('.//@class').extract_first().split('-')[-1]
            item['hot'] = response.css('.app-intro-comment').xpath('text()').extract_first('').strip('\(\) ')
            yield item
        except Exception as e:
            logging.exception(e)


