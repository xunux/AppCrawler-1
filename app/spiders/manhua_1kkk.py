# -*- coding: utf-8 -*-
import scrapy
import re
import logging
import json
import execjs

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors.sgml import SgmlLinkExtractor
from scrapy.linkextractors import LinkExtractor
from scrapy.http import Request

from app.items import ManhuaItem
from app.items import ImageItem

class Manhua1kkkSpider(CrawlSpider):
    """
        漫画爬虫
    """
    name = "1kkk"
    allowed_domains = ["m.1kkk.com", 'cdnmd5.com']
    start_urls = [
        'http://m.1kkk.com/manhua-new/',
        'http://m.1kkk.com/search',
        'http://m.1kkk.com/',
    ]

    # 过滤掉js 代码中的一个空格
    js_regex = re.compile('\}\(\'[a-zZ-Z0-9]+ [a-zA-Z0-9]+=')

    rules = [
        # Rule(LinkExtractor(allow=("http://m\.1kkk\.com$", )), callback='parse', follow=True),
        Rule(LinkExtractor(allow=("http://m\.1kkk\.com/manhua-\w+", )), callback='parse', follow=True),
        Rule(LinkExtractor(allow=("http://m\.1kkk\.com/manhua\d+", )), callback='parse_manhua', follow=True),
        Rule(LinkExtractor(allow=("http://m\.1kkk\.com/ch\d+-\d+(-\w+)*", )), callback='parse_manhua_info', follow=True),
    ]

    def parse_manhua_info(self, response):
        # print response.text
        """
        解析漫画具体章节下的漫画详情，获取漫画图片链接，链接是通过混淆过的js自动计算出来的。

        引入pyexecjs 库解析js
        js混淆解密，发现js代码其实就是声明了一个 var newImgs = []的数组。参考： http://tool.chinaz.com/js.aspx
        :param response:
        :return:
        """

        js_code = response.css('body > script:nth-child(8)').xpath('.//text()').extract_first()
        # js_code = self.js_regex.sub(lambda m: m.group().replace(' ', ''), js_code) # 过滤掉空格
        image_urls = execjs.eval(js_code + ', newImgs')
        item = ImageItem()
        item['url'] = response.url
        item['name'] = response.css("#title").xpath('text()').extract_first('').split(' ')[0]
        item['chapter'] = filter(lambda x:x.isdigit(), response.css("#title").xpath('text()').extract_first('').split(' ')[1])
        item['image_urls'] = image_urls
        # print image_urls
        yield item

    def parse_manhua(self, response):
        try:
            item = ManhuaItem()
            item['url'] = response.url
            item['name'] = response.css('.detailForm .main .info p.title').xpath('.//text()').extract_first('').strip()
            item['info'] = " ".join(response.css('.details ul li').xpath('.//text()').extract()).strip()
            item['category'] = response.css('.detailForm .main .info p.subtitle').xpath('.//text()').extract()[0].split(u"：")[1].strip()
            item['author'] = response.css('.detailForm .main .info p.subtitle').xpath('.//text()').extract()[1].split(u"：")[1].strip()
            item['icon'] = response.css('.coverForm img').xpath('@src').extract_first()
            c_keys = [s.strip().replace('.', '_') for s in response.css('.chapters ul li a').xpath('text()').extract()]
            c_values = response.css('.chapters ul li a').xpath('@href').extract()
            item['chapters'] = dict(zip(c_keys, c_values))
            item['introduce'] = response.css('.detailContent >p').xpath('text()').extract_first('').strip()
            # item['star_num'] = response.css('.intro-titles .star1-empty div').xpath('.//@class').extract_first().split('-')[-1]
            item['comments'] = [' '.join(filter(lambda s: s.strip(), sel.xpath('.//text()').extract())) for sel in response.css('.commentList ul.list li')]
            yield item
        except Exception as e:
            logging.exception(e)


