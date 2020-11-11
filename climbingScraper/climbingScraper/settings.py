# -*- coding: utf-8 -*-

# Scrapy settings for climbingScraper project
#


import os
from os.path import join, dirname
from dotenv import load_dotenv

BOT_NAME = 'climbingScraper'

SPIDER_MODULES = ['climbingScraper.spiders']
NEWSPIDER_MODULE = 'climbingScraper.spiders'

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINE = {
    'scrapy.pipelines.files.S3FilesStore':100,
}

FEED_URI = 's3://mpcrawlerdump/%(name)s/%(time)s.csv'
FEED_FORMAT = 'csv'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 2

# Disable cookies (enabled by default)
COOKIES_ENABLED = False
