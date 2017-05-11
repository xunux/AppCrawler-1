# -*- coding: utf-8 -*-
import scrapy
import re

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.linkextractors import LinkExtractor
from app.items import HiapkItem


class HiapkAppSpider(CrawlSpider):
    name = "hiapk_app"
    allowed_domains = ["hiapk.com"]
    start_urls = [
        # 'http://apk.hiapk.com/apps',
        'http://apk.hiapk.com/apps/MediaAndVideo',
        'http://apk.hiapk.com/apps/DailyLife',
        'http://apk.hiapk.com/apps/Social',
        'http://apk.hiapk.com/apps/Education',
        'http://apk.hiapk.com/apps/Finance',
        'http://apk.hiapk.com/apps/Tools',
        'http://apk.hiapk.com/apps/TravelAndLocal',
        'http://apk.hiapk.com/apps/Communication',
        'http://apk.hiapk.com/apps/Shopping',
        'http://apk.hiapk.com/apps/Reading',
        'http://apk.hiapk.com/apps/NewsAndMagazines',
        'http://apk.hiapk.com/apps/HealthAndFitness',
        'http://apk.hiapk.com/apps/AntiVirus',
        'http://apk.hiapk.com/apps/Browser',
        'http://apk.hiapk.com/apps/Productivity',
        'http://apk.hiapk.com/apps/Productivity?sort=5&pi=7',
        'http://apk.hiapk.com/apps/Personalization',
        'http://apk.hiapk.com/apps/Input',
        'http://apk.hiapk.com/apps/Photography',
        
        # 'http://apk.hiapk.com/games',
        'http://apk.hiapk.com/games/OnlineGames',
        'http://apk.hiapk.com/games/Casual',
        'http://apk.hiapk.com/games/RolePlaying',
        'http://apk.hiapk.com/games/BrainAndPuzzle',
        'http://apk.hiapk.com/games/Shooting',
        'http://apk.hiapk.com/games/Sports',
        'http://apk.hiapk.com/games/Children',
        'http://apk.hiapk.com/games/Chess',
        'http://apk.hiapk.com/games/Strategy',
        'http://apk.hiapk.com/games/Simulation',
        'http://apk.hiapk.com/games/Racing',
    ]
    rules = [
       # Rule(LinkExtractor(allow=("http://apk\.hiapk\.com/appinfo/", )), callback='parse_app',follow=True),
       #  Rule(LinkExtractor(allow=("http://apk\.hiapk\.com/apps?sort=\d+&pi=\d+", )), callback='parse',follow=True),
       #  Rule(LinkExtractor(allow=("http://apk\.hiapk\.com/games.*?sort=\d+&pi=\d+", )), callback='parse',follow=True),
        Rule(LinkExtractor(allow=("http://apk\.hiapk\.com/apps/", )), callback='parse_sim',follow=True),
        Rule(LinkExtractor(allow=("http://apk\.hiapk\.com/games/", )), callback='parse_sim',follow=True),
    ]

    def start_requests(self):
        for base_url in self.start_urls:
            for ra in range(1,6):
                for i in [5, 8, 9]:
                        url = base_url + "?sort=" + str(i) + "&ra=" + str(ra)
                        yield self.make_requests_from_url(url)

    def parse_sim(self, response):
        selector_list = response.css('#appSoftListBox .list_item')
        for sel in selector_list:
            item = HiapkItem()
            item['url'] = response.url
            item['package'] = sel.css('.list_content a').xpath('@href').extract_first("").split('/')[2]
            item['apk_url'] = 'http://apk.hiapk.com/appinfo/' + item['package']
            item['name'] = sel.css('.list_content .list_title a').xpath('text()').extract_first("")
            item['version'] = sel.css('.list_content .list_version').xpath('text()').extract_first("").strip('\(\)')
            item['publish_date'] = sel.css('.list_content .push_time').xpath('text()').extract_first("").strip('\(\)')[0:10]
            item['category'] = " ".join(
                [response.css('.nav_menu .on a').xpath('@title').extract_first("").split("-")[0],
                 response.css('.category_item.on a span:nth-child(2)').xpath("text()").extract_first(""), ])
            item['introduce'] = sel.css('.list_content .list_description').xpath('text()').extract_first("").strip()
            yield item


  
