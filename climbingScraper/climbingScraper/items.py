# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ClimbingscraperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

# Initializes scrapy Items for tickScraper spider
class tickData(scrapy.Item):
    user_id = scrapy.Field()
    route_id = scrapy.Field()
    route_type = scrapy.Field()
    route_grade = scrapy.Field()
    route_notes = scrapy.Field()

class routeData(scrapy.Item):
    route_id = scrapy.Field()
    route_name = scrapy.Field()
    route_grade = scrapy.Field()
