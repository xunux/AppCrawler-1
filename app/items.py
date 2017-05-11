# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class AppItem(scrapy.Item):
    apk_url  = scrapy.Field()
    name     = scrapy.Field()
    rate     = scrapy.Field()
    category = scrapy.Field()
    size     = scrapy.Field()
    url      = scrapy.Field()
    screenshots  = scrapy.Field()
    download_num = scrapy.Field()


class GoogleItem(scrapy.Item):
    url = scrapy.Field()
    num = scrapy.Field()


class HiapkItem(scrapy.Item):
    name = scrapy.Field()
    package = scrapy.Field()
    publish_date = scrapy.Field()
    version = scrapy.Field()
    is_new = scrapy.Field()
    url = scrapy.Field()
    apk_url = scrapy.Field()
    qr_code_url = scrapy.Field()
    category = scrapy.Field()
    apk_size = scrapy.Field()
    hot = scrapy.Field()
    star_num = scrapy.Field()
    introduce = scrapy.Field()
    imprint = scrapy.Field()
    info = scrapy.Field()


class WandoujiaItem(scrapy.Item):
    name = scrapy.Field()
    is_new = scrapy.Field()
    icon = scrapy.Field()
    url = scrapy.Field()
    apk_url = scrapy.Field()
    qr_code_url = scrapy.Field()
    version = scrapy.Field()
    category1 = scrapy.Field()
    category2 = scrapy.Field()
    category = scrapy.Field()
    tags = scrapy.Field()
    company = scrapy.Field()
    publish_date = scrapy.Field()
    apk_size = scrapy.Field()
    download_num = scrapy.Field()
    hot = scrapy.Field()
    love_num = scrapy.Field()
    comments_num = scrapy.Field()
    star_num = scrapy.Field()
    introduce = scrapy.Field()
    imprint = scrapy.Field()
    info = scrapy.Field()


class CoolapkItem(scrapy.Item):
    name = scrapy.Field()
    package = scrapy.Field()
    publish_date = scrapy.Field()
    version = scrapy.Field()
    icon = scrapy.Field()
    is_new = scrapy.Field()
    url = scrapy.Field()
    apk_url = scrapy.Field()
    qr_code_url = scrapy.Field()
    category = scrapy.Field()
    tags = scrapy.Field()
    company = scrapy.Field()
    apk_size = scrapy.Field()
    download_num = scrapy.Field()
    hot = scrapy.Field()
    love_num = scrapy.Field()
    comments_num = scrapy.Field()
    editor_comment = scrapy.Field()
    star_num = scrapy.Field()
    introduce = scrapy.Field()
    imprint = scrapy.Field()
    info = scrapy.Field()


class XiaomiAppItem(scrapy.Item):
    name = scrapy.Field()
    appid = scrapy.Field()
    package = scrapy.Field()
    publish_date = scrapy.Field()
    version = scrapy.Field()
    icon = scrapy.Field()
    is_new = scrapy.Field()
    url = scrapy.Field()
    apk_url = scrapy.Field()
    qr_code_url = scrapy.Field()
    top_category = scrapy.Field()
    category = scrapy.Field()
    tags = scrapy.Field()
    company = scrapy.Field()
    apk_size = scrapy.Field()
    download_num = scrapy.Field()
    hot = scrapy.Field()
    love_num = scrapy.Field()
    comments_num = scrapy.Field()
    editor_comment = scrapy.Field()
    star_num = scrapy.Field()
    introduce = scrapy.Field()
    imprint = scrapy.Field()
    info = scrapy.Field()