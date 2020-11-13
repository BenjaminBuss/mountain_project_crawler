# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


# Initializes scrapy Items for tickScraper spider
class tickData(scrapy.Item):
    user_id = scrapy.Field()
    route_id = scrapy.Field()
    route_type = scrapy.Field()
    route_grade = scrapy.Field()
    route_notes = scrapy.Field()

class routeData(scrapy.Item):
    id_route = scrapy.Field()
    name_route = scrapy.Field()
    grade_route = scrapy.Field()

class userTicks(scrapy.Item):
    user = scrapy.Field()
    route = scrapy.Field()
