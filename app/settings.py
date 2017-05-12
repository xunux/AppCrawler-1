# -*- coding: utf-8 -*-

# Scrapy settings for app project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'app'

SPIDER_MODULES = ['app.spiders']
NEWSPIDER_MODULE = 'app.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'app (+http://www.yourdomain.com)'

ITEM_PIPELINES = {
  # 'app.pipelines.AppPipeline':1,
  'scrapy_mongodb.MongoDBPipeline' : 100,
}

# 参考 https://github.com/sebdah/scrapy-mongodb/blob/master/README.md
MONGODB_URI = 'mongodb://127.0.0.1:27017'
MONGODB_DATABASE = 'scrapy'
MONGODB_COLLECTION = 'item'
# MONGODB_UNIQUE_KEY = 'url'
MONGODB_ADD_TIMESTAMP = True

EXTENSIONS = {'scrapy.contrib.feedexport.FeedExporter': None}

DOWNLOADER_MIDDLEWARES = {
            'scrapy.contrib.downloadermiddleware.redirect.RedirectMiddleware': 600,
            'scrapy.contrib.downloadermiddleware.httpproxy.HttpProxyMiddleware': 110,
            'app.middlewares.ProxyMiddleware': 100
                        }

PROXIES = [
    # {'ip_port': '104.128.81.60:7777', 'user_pass': None},
    {'ip_port': '127.0.0.1:8087', 'user_pass': None},
    # {'ip_port': '123.57.190.51:7777', 'user_pass': None},
    # {'ip_port': '218.30.99.209:81', 'user_pass': None},

    # {'ip_port': '60.169.78.218:808', 'user_pass': None},    #安徽芜湖 686
    # {'ip_port': '119.254.84.90:80', 'user_pass': None},  # 北京 1238天
]

LOG_ENCODING = 'UTF-8'
# LOG_FILE = 'app.log'
LOG_ENABLED = True
LOG_STDOUT = True
