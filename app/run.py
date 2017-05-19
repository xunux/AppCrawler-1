#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
Topic: sample
Desc : 
"""

import logging
from spiders.hiapk_app import HiapkAppSpider
from spiders.hiapk import HiapkInfoSpider
from spiders.coolapk import CoolpakSpider
from spiders.manhua_1kkk import Manhua1kkkSpider
from spiders.coolapk_info import CoolpakInfoSpider
from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
from scrapy.utils.log import configure_logging

from sqlalchemy.orm import sessionmaker

if __name__ == '__main__':
    settings = get_project_settings()
    configure_logging(settings)

    runner = CrawlerRunner(settings)

    # spider = ArticleSpider(rule)  # instantiate every spider using rule
    # stop reactor when spider closes
    # runner.signals.connect(spider_closing, signal=signals.spider_closed)
    # runner.crawl(CoolpakSpider)
    # runner.crawl(CoolpakInfoSpider)
    runner.crawl(Manhua1kkkSpider)

    d = runner.join()
    d.addBoth(lambda _: reactor.stop())

    # blocks process so always keep as the last statement
    reactor.run()
    logging.info('all finished.')
