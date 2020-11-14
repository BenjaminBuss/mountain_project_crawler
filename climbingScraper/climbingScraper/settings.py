# -*- coding: utf-8 -*-

# Scrapy settings for climbingScraper project
#

import os
from os.path import join, dirname
from dotenv import load_dotenv

BOT_NAME = 'climbingScraper'

SPIDER_MODULES = ['climbingScraper.spiders']
NEWSPIDER_MODULE = 'climbingScraper.spiders'

LOG_LEVEL = 'INFO'

# AWS Authentication
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")

AWS_REGION_NAME = 'us-east-2'

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
FEED_EXPORT_BATCH_ITEM_COUNT = 10000

ITEM_PIPELINE = {
#   'climbingScraper.pipelines.S3Multi': 1,
    'scrapy.pipelines.files.S3FilesStore': 100,
}

# https://docs.scrapy.org/en/latest/topics/feed-exports.html#feeds
# FEEDS = {
#     's3://mpcrawlerdump/%(name)s/routeData/%(batch_id)s%(batch_time)s.json': {
#         'format': 'jsonlines',
#         'encoding': 'utf8',
#         'fields': ['id_route', 'name_route', 'grade_route', 'stars_route', 'type_route', 'fa_route', 'views_route', 'date_route'],
#     },
#     's3://mpcrawlerdump/%(name)s/userTicks/%(batch_time)s.json': {
#         'format': 'jsonlines',
#         'encoding': 'utf8',
#         'fields': ['user', 'route'],
#     },
#     's3://mpcrawlerdump/%(name)s/tickData/%(batch_time)s.json': {
#         'format': 'jsonlines',
#         'encoding': 'utf8',
#         'fields': ['user_id', 'route_id', 'route_type', 'route_grade', 'route_notes', 'route_name'],
#     },
# }

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
DOWNLOAD_DELAY = 2

# Disable cookies (enabled by default)
COOKIES_ENABLED = False

# DOESN'T DIFFERENTIATE ITEMS AT ALL
FEED_URI = 's3://mpcrawlerdump/%(name)s/jsonData/%(batch_time)s.json'
FEED_FORMAT = 'jsonlines'
