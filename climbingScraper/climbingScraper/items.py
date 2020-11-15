# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

# Initializes scrapy Items for tickScraper spider
class routeData(scrapy.Item):
    id = scrapy.Field()
    route_id = scrapy.Field()
    route_name = scrapy.Field()
    route_grade = scrapy.Field()
    route_stars = scrapy.Field()
    route_type = scrapy.Field()
    route_fa = scrapy.Field()
    route_views = scrapy.Field()
    route_share = scrapy.Field()

class userTicks(scrapy.Item):
    id = scrapy.Field()
    user_id = scrapy.Field()
    route_id = scrapy.Field()

class tickData(scrapy.Item):
    id = scrapy.Field()
    user_id = scrapy.Field()
    route_id = scrapy.Field()
    route_type = scrapy.Field()
    route_grade = scrapy.Field()
    route_notes = scrapy.Field()
    route_name = scrapy.Field()
