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

# https://docs.scrapy.org/en/latest/topics/feed-exports.html#feeds
FEEDS = {
    's3://mpcrawlerdump/%(name)s/tickData/%(time)s.csv': {
        'format': 'csv',
        'fields': ['user_id', 'route_id', 'route_type', 'route_grade', 'route_notes'],
    },
    's3://mpcrawlerdump/%(name)s/routeData/%(time)s.csv': {
        'format': 'csv',
        'fields': ['id_route', 'name_route', 'grade_route'],
    },
    's3://mpcrawlerdump/%(name)s/userTicks/%(time)s.csv': {
        'format': 'csv',
        'fields': ['user', 'route'],
    },
}


# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
DOWNLOAD_DELAY = 2

# Disable cookies (enabled by default)
COOKIES_ENABLED = False

# DOESN'T DIFFERENTIATE ITEMS AT ALL
#FEED_URI = 's3://mpcrawlerdump/%(name)s/tickData/%(time)s.csv'
#FEED_FORMAT = 'csv'
