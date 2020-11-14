# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
# Thanks https://stackoverflow.com/questions/32743469/scrapy-python-multiple-item-classes-in-one-pipeline

from .items import tickData, routeData, userTicks
from scrapy.pipelines.files import S3FilesStore


#class MultiS3(object):
#    def process_item(self, item, spider):
#        return item

#    def process_item(self, item, spider):
#        if isinstance(item, tickData):
#            return self.handleTick(item, spider)
#        if isinstance(item, routeData):
#            return self.handleRoute(item, spider)
#        if isinstance(item, userTicks):
#            return self.handleUT(item,spider)

#    def handleTick(self, item):
        # Handle Comment here, return item
#        return item

#    def handleRoute(self, item):
        # Handle profile here, return item
#        return item

#    def handleUT(self, item):
        # Handle user tick data
#        return item
