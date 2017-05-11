# -*- coding: utf-8 -*-
import scrapy
import re

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.linkextractors import LinkExtractor
from app.items import HiapkItem


class HiapkInfoSpider(CrawlSpider):
    name = "hiapk_info"
    allowed_domains = ["hiapk.com"]
    start_urls = [
        'http://apk.hiapk.com/apps',
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

        'http://apk.hiapk.com/games',
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
        Rule(LinkExtractor(allow=("http://apk\.hiapk\.com/appinfo/", )), callback='parse_app',follow=True),
        Rule(LinkExtractor(allow=("http://apk\.hiapk\.com/apps?sort=\d+&pi=\d+", )), callback='parse',follow=True),
        Rule(LinkExtractor(allow=("http://apk\.hiapk\.com/games.*?sort=\d+&pi=\d+", )), callback='parse',follow=True),
        Rule(LinkExtractor(allow=("http://apk\.hiapk\.com/apps", )), callback='parse',follow=True),
        Rule(LinkExtractor(allow=("http://apk\.hiapk\.com/games", )), callback='parse',follow=True),
    ]

    def start_requests(self):
        for base_url in self.start_urls:
            for ra in range(1,6):
                for i in [5, 8, 9]:
                        url = base_url + "?sort=" + str(i) + "&ra=" + str(ra)
                        yield self.make_requests_from_url(url)

    def parse_app(self, response):
        item = HiapkItem()
        item['url'] = response.url
        item['is_new'] = 0 if re.search('/[a-zA-Z0-9_\-\.]+/\d+$', response.url) else 1
        item['package'] = response.css("#appInfoDownUrl").xpath("@href").extract_first("").split('/')[2]
        item['apk_url'] = 'http://apk.hiapk.com' + response.css("#appInfoDownUrl").xpath("@href").extract_first("")
        full_name = response.css("#appSoftName").xpath("text()").extract_first("").strip()
        start_index = full_name.find('(')
        end_index = full_name.find(')')
        item['name'] = full_name[0:start_index]
        item['version'] = full_name[start_index+1:end_index]
        item['qr_code_url'] = response.css("img#QRCode").xpath("@src").extract_first("").strip()
        item['apk_size'] = response.css("#appSize").xpath("text()").extract_first("").strip()
        item['hot'] = response.css(".line_content:nth-child(3) span:nth-child(2)").xpath("text()").extract_first("").strip()
        item['category'] = " ".join(response.css(".detail_tip").xpath(".//a[position()>1]/text()").extract())
        item['info'] = response.css(".line_content  span").xpath("text()").extract()
        item['introduce'] = response.css("#softIntroduce").xpath("text()").extract_first("").strip()
        item['imprint'] = response.css("#softImprint pre").xpath("text()").extract_first("").strip()
        item['star_num'] = response.css(".star_num").xpath("text()").extract_first("").strip()
        yield item


  
