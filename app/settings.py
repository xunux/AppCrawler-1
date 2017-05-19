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

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

COOKIES_ENABLES = False

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'app (+http://www.yourdomain.com)'
USER_AGENT_LIST = [
    # pc browser user agents
    # 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36',
    # 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.54 Safari/536.5',
    # 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/537.75.14',
    # 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:29.0) Gecko/20100101 Firefox/29.0',
    # 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.137 Safari/537.36',
    # 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:28.0) Gecko/20100101 Firefox/28.0',

    # mobile browser user agents
    'Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1',
    'Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 5.1.1; Nexus 6 Build/LYZ28E) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 5.1.1; Nexus 6 Build/LYZ28E) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Mobile Safari/537.36',
]

EXTENSIONS = {
    'scrapy.contrib.feedexport.FeedExporter': None,
    'app.extensions.throttle.AutoThrottleWithList': 300,
}

DOWNLOADER_MIDDLEWARES = {
    'scrapy.contrib.downloadermiddleware.redirect.RedirectMiddleware': 600,
    'scrapy.contrib.downloadermiddleware.httpproxy.HttpProxyMiddleware': 110,
    'app.middlewares.ProxyMiddleware': 10,
    'app.middlewares.RandomUserAgent': 1,
}

ITEM_PIPELINES = {
  # 'app.pipelines.AppPipeline':1,
  # 'app.pipelines.MyImagesPipeline':1,
  # 'scrapy_mongodb.MongoDBPipeline': 100,
  'app.scrapy_mongodb.MongoDBPipeline': 100,
  'app.pipelines.MyImagesPipeline': 1,
}

IMAGES_STORE = 'E:\\data\\images'   # 图片存储路径
FILES_EXPIRES = 90
IMAGES_EXPIRES = 90                                   # 过期天数
# 图片缩略图
IMAGES_THUMBS = {
    'small': (50, 50),
    'big': (270, 270),
}
IMAGES_MIN_HEIGHT = 400                               # 图片的最小高度
IMAGES_MIN_WIDTH = 400                                # 图片的最小宽度


# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 32
# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# DOWNLOAD_DELAY = 3
CONCURRENT_REQUESTS_PER_DOMAIN = 32
#CONCURRENT_REQUESTS_PER_IP = 16

# Enable and configure the AutoThrottle extension (disabled by default)
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 0.25
AUTOTHROTTLE_MAX_DELAY = 10
# Enable showing throttling stats for every response received:
AUTOTHROTTLE_DEBUG = True


LIMIT_SITES = {
	'm.1kkk.com': 0
}


# 参考 https://github.com/sebdah/scrapy-mongodb/blob/master/README.md
MONGODB_URI = 'mongodb://127.0.0.1:27017'
MONGODB_DATABASE = 'scrapy'
MONGODB_COLLECTION = 'item'
MONGODB_UNIQUE_KEY = 'url'
MONGODB_ADD_TIMESTAMP = True

PROXY_SITES = [
    'm.1kkk.com',
]
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
