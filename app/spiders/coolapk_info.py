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
    name = "coolapk_info"
    allowed_domains = ["coolapk.com"]
    start_urls = [
        'http://www.coolapk.com/apk/',
        'http://www.coolapk.com/game/',
    ]

    rules = [
       # Rule(LinkExtractor(allow=("http://apk\.hiapk\.com/appinfo/", )), callback='parse_app',follow=True),
       #  Rule(LinkExtractor(allow=("http://apk\.hiapk\.com/apps?sort=\d+&pi=\d+", )), callback='parse',follow=True),
       #  Rule(LinkExtractor(allow=("http://apk\.hiapk\.com/games.*?sort=\d+&pi=\d+", )), callback='parse',follow=True),
        Rule(LinkExtractor(allow=("http://www\.coolapk\.com/apk/\?p=\d+", )), callback='parse',follow=True),
        Rule(LinkExtractor(allow=("http://www\.coolapk\.com/game/\?p=\d+", )), callback='parse',follow=True),
        Rule(LinkExtractor(allow=("http://www\.coolapk\.com/game/[a-zA-Z0-9_\-\.]+", )), callback='parse_app',follow=True),
        Rule(LinkExtractor(allow=("http://www\.coolapk\.com/apk/[a-zA-Z0-9_\-\.]+", )), callback='parse_app',follow=True),
    ]

    def parse_app(self, response):
        selector_list = response.css('div.row >div:nth-child(1) .panel ul.media-list li')
        try:
            item = CoolapkItem()
            item['url'] = response.url
            item['name'] = response.css('div.ex-page-header div.container .media-body h1 small').xpath('text()').extract_first('')
            item['info'] = ' '.join(response.css('div.ex-page-header div.container .media-body .media-intro span').xpath('text()').extract())
            item['editor_comment'] = response.css('.ex-container .row').xpath('.//div[1]/div[2]/text()').extract_first()
            item['info'] += "".join([x.strip(' ') for x in response.css('#ex-apk-detail-pane').xpath('.//text()').extract()]).strip() \
                + "".join([x.strip(' ') for x in response.css('#ex-apk-permission-pane').xpath('.//text()').extract()]).strip()
            item['introduce'] = '<br/>'.join(response.css('.ex-card-content').xpath('.//p/text()').extract())
            item['category'] = category_dict.get(response.url.split('/')[-2])
            c_tags = response.css('div.row .col-md-5').xpath('.//div[6]/div[3]/a')
            for c_tag in c_tags:
                c_tag_name = c_tag.xpath('text()').extract_first('')
                c_tag_url = c_tag.xpath('@href').extract_first('')
                if c_tag_url.find('tag'):
                    item['tags'] += c_tag_name
                else:
                    item['category'] += c_tag_name

            item['imprint'] = ''.join(response.css('div.row .col-md-5').xpath('.//div[6]/div[5]/text()').extract()).strip()
            item['apk_url'] = response.url
            item['icon'] = response.css('div.ex-page-header div.container img.media-object').xpath('@src').extract_first('')
            item['package'] = response.url.split('/')[-1]
            item['version'] = response.css('div.ex-page-header div.container .media-body h1 small').xpath('text()').extract_first('')
            item['apk_size'] = response.css('#ex-apk-detail-pane dl').xpath('.//dd[6]/text()').extract_first('')
            item['star_num'] = response.css('#ex-apk-rank-pane div span:nth-child(2)').xpath('text()').extract_first('')
            item['download_num'] = response.css('div.ex-page-header div.container .media-body .media-intro span').xpath('text()').extract()[0].split(u'，')[1].rstrip(u'次下载')
            yield item
        except Exception as e:
            raise e


  
