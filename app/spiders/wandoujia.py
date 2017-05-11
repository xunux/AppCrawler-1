# -*- coding: utf-8 -*-
import scrapy
import re

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors.sgml import SgmlLinkExtractor
from scrapy.linkextractors import LinkExtractor
from app.items import WandoujiaItem

category1_dict = {
    u"系统工具": u"应用",
    u"视频": u"应用",
    u"聊天社交": u"应用",
    u"新闻阅读": u"应用",
    u"购物": u"应用",
    u"旅游出行": u"应用",
    u"音乐": u"应用",
    u"交通导航": u"应用",
    u"金融理财": u"应用",
    u"教育培训": u"应用",
    u"图像": u"应用",
    u"生活实用工具": u"应用",
    u"生活服务": u"应用",
    u"效率办公": u"应用",
    u"美化手机": u"应用",
    u"运动健康": u"应用",
    u"电话通讯": u"应用",
    u"丽人母婴": u"应用",

    u"休闲时间": u"游戏",
    u"跑酷竞速": u"游戏",
    u"宝石消除": u"游戏",
    u"网络游戏": u"游戏",
    u"动作射击": u"游戏",
    u"扑克棋牌": u"游戏",
    u"儿童益智": u"游戏",
    u"塔防守卫": u"游戏",
    u"体育格斗": u"游戏",
    u"角色扮演": u"游戏",
    u"经营策略": u"游戏",
}


class WandoujiaSpider(CrawlSpider):
    name = "wandoujia"
    allowed_domains = ["wandoujia.com"]
    start_urls = (
        'http://www.wandoujia.com/category/app/',
        'http://www.wandoujia.com/category/game/',
    )

    rules = [
        # 匹配 http://www.wandoujia.com/apps/com.freeapp.batterysaver 但过滤掉 以.html结尾的链接，
        # 如   http://www.wandoujia.com/apps/com.freeapp.batterysaver.html
        Rule(LinkExtractor(allow=("http://www\.wandoujia\.com/apps/(?![a-zA-Z0-9_\-\.]+?\.html)[a-zA-Z0-9_\-\.]*$",)),
             callback='parse_app', follow=True),
        Rule(LinkExtractor(allow=(r"http://www\.wandoujia\.com/category/app",)), callback='parse', follow=True),
        Rule(LinkExtractor(allow=("http://www\.wandoujia\.com/category/game",)), callback='parse', follow=True),
        Rule(LinkExtractor(allow=("http://www\.wandoujia\.com/category/[0-9_]+$",)), callback='parse', follow=True),
    ]

    def parse_app(self, response):
        item = WandoujiaItem()
        item['url'] = response.url
        item['is_new'] = 0 if re.search('/[a-zA-Z0-9_\-\.]+/\d+$', response.url) else 1
        item['apk_url'] = response.css('.qr-info a').xpath('@href').extract_first('')
        item['icon'] = response.css('.app-icon img').xpath('@src').extract_first('')
        item['name'] = response.css('.app-name span').xpath('text()').extract_first('')
        item['qr_code_url'] = response.css('.qr-info img').xpath('@src').extract_first('')
        item['apk_size'] = response.css('div.infos dl.infos-list dd').xpath('text()').extract()[0].strip()

        # item['hot'] = response.css(".line_content:nth-child(3) span:nth-child(2)").xpath("text()").extract_first("").strip()
        item['category2'] = response.css("div.crumb > div.second > a > span").xpath("text()").extract_first('')
        item['category1'] = category1_dict.get(item['category2'])
        item['category'] = " ".join(response.css(".infos-list dd.tag-box a").xpath("text()").extract())
        item['tags'] = " ".join(
            [i.strip() for i in response.css(".infos-list .side-tags .tag-box a").xpath("text()").extract()])
        # item['publish_date'] = response.css('div.infos dl.infos-list dd time').xpath('@datetime').extract_first('')
        item['publish_date'] = response.css('div.infos dl.infos-list dd time').xpath('text()').extract_first('')
        item['version'] = response.css('div.infos dl.infos-list > dd:nth-child(10)').xpath('text()').extract_first('')
        item['company'] = response.css('div.infos dl.infos-list > dd span[itemprop=name]').xpath(
            'text()').extract_first('')
        item['info'] = response.css("div.infos dl.infos-list dd ").xpath("text()").extract()
        item['introduce'] = '<br/>'.join(
            [x.strip() for x in response.css(".desc-info div[itemprop=description]").xpath("text()").extract()])
        item['imprint'] = '<br/>'.join([x.strip() for x in response.css(".change-info div").xpath("text()").extract()])
        item['star_num'] = response.css(".num-list .score-container meta[itemprop=ratingValue]").xpath(
            "@content").extract_first("").strip()
        item['download_num'] = response.css('.num-list .item i').xpath('text()').extract()[0]
        item['love_num'] = response.css('.num-list .item i').xpath('text()').extract()[1]
        item['comments_num'] = response.css('.num-list .item i').xpath('text()').extract()[2]
        yield item



