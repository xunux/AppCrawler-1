# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem
from scrapy.http import Request
import re

class AppPipeline(object):
    def process_item(self, item, spider):
        # print item.__class__.__name__
        return item

class MyImagesPipeline(ImagesPipeline):
    """先安装：pip install Pillow"""

    file_filter_regex = re.compile('[\\\/:*?"<>|]')
    def get_media_requests(self, item, info):
        for num, image_url in enumerate(item.get(self.images_urls_field, [])):
            # yield Request(image_url, headers={'Referer': 'http://www.manben.com/'}, meta={'item': item, 'num': num+1})
            yield Request(image_url, headers={'Referer': item['url']}, meta={'item': item, 'num': num+1})

    # def item_completed(self, results, item, info):
    #     image_paths = [x['path'] for ok, x in results if ok]
    #     if not image_paths:
    #         raise DropItem("Item contains no images")
    #     return item

    def file_path(self, request, response=None, info=None):
        item = request.meta['item']
        num = request.meta['num']
        # 从URL提取图片的文件名
        image_guid = request.url.split('?')[0].split('/')[-1].split('_')[0]
        # 拼接最终的文件名,格式:full/{书名}/{章节}/图片文件名.jpg
        name = self.file_filter_regex.sub('', item['name'])
        filename = u'full/{0}/{1[chapter]}/{2}.jpg'.format(name, item, num)
        return filename