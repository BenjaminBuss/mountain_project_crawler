# Benjamin Buss
# October 25th 2020
# Mountain Project Scraping idea draft


import scrapy
#from scrapy.crawler import CrawlerProcess
#import numpy as np
import re
#import scrapy_proxies


def strip_id(url):
    temp_regex = re.findall(r'\d+', url)
    temp_stripped = list(map(int, temp_regex))
    return temp_stripped


def return_ele(x):
    try:
        return x[1]
    except IndexError:
        return 1


route_info = []  # np.array()
area_codes = []  # np.array()
route_codes = []  # np.array()
user_codes = []  # np.array()


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


class ProjectSpider(scrapy.Spider):
    name = 'mpScraper'
    allowed_domains = ['mountainproject.com']
    #start_urls = ['https://www.mountainproject.com/area/118272520/wales-canyon']

    route_info = []  # np.array()
    area_codes = []  # np.array()
    route_codes = []  # np.array()
    user_codes = []  # np.array()

    def __init__(self, domain='', pages='10', *args, **kwargs):
        super(ProjectSpider, self).__init__(*args, **kwargs)
        #self.start_urls = [f'https://www.mountainproject.com/area/{domain}']
        self.start_urls = [f'{domain}']
        self.page_max = int(f'{pages}')

    def parse(self, response):
        # area_name = response.css('div.mp-sidebar a[href*=area] ::text').getall()
        area_link = response.css('div.mp-sidebar a[href*=area]::attr(href)').getall()

        if len(area_link) <= 0:
            route_link = response.css('div.mp-sidebar a[href*=route]::attr(href)').getall()
            for url in route_link:
                if strip_id(url) in route_codes:
                    break
                else:
                    route_codes.append(strip_id(url))
                    yield response.follow(url=url, callback=self.parse_routes)
        else:
        # Iterate through subarea urls, add to an array, send them to be parsed
            for url in area_link:
                area_codes.append(strip_id(url))
                yield response.follow(url=url, callback=self.parse_subareas)

    def parse_subareas(self, response):
        area_link = response.css('div.mp-sidebar a[href*=area]::attr(href)').getall()
        route_link = response.css('div.mp-sidebar a[href*=route]::attr(href)').getall()

        if len(area_link) == 0 and len(route_link) != 0:
            for url in route_link:
                if strip_id(url) in route_codes:
                    break
                else:
                    route_codes.append(strip_id(url))
                    yield response.follow(url=url, callback=self.parse_routes)
        else:
            for url in area_link:
                if strip_id(url) in area_codes:
                    break
                else:
                    area_codes.append(strip_id(url))
                    yield response.follow(url=url, callback=self.parse_subareas)

    def parse_routes(self, response):
        route_name = response.css('div.col-md-9.float-md-right.mb-1 h1::text').get().strip()
        route_grade = response.css("span.rateYDS::text").get()
        #route_stars = response.css("[id='route-star-avg'] *::text").getall()  # needs some cleaning
        # route_share = GET SHARED DATE?? IT'S IN A TABLE

        route_subinfo = response.css('a.show-tooltip ::attr(href)').get()

        route_id = int(strip_id(route_subinfo)[0])

        route_info = routeData()
        route_info['route_id'] = route_id
        route_info['route_name'] = route_name
        route_info['route_grade'] = route_grade

        yield route_info

        yield response.follow(url=route_subinfo, callback=self.get_users)

    def get_users(self, response):
        route_id = strip_id(response.url)
        route_ticks = response.css('.col-lg-6  a[href*=user]::attr(href)').getall()

        for url in route_ticks:
            user_id = strip_id(url)

            yield {'route_id': route_id[0], 'user_id': user_id}

            if user_id in user_codes:
                break
            else:
                user_codes.append(user_id)
                yield response.follow(url=url, callback=self.open_user)

    def open_user(self, response):
        user_ticks = response.css('div.section-title a[href*=ticks]::attr(href)').getall()

        for url in user_ticks:
            yield response.follow(url=url, callback=self.parse_user)

    def parse_user(self, response):
        stripped = strip_id(response.url)
        user_id = stripped[0]
        user_ticks = response.css('a[href*=route]::attr(href)').getall()
        tick_grades = response.css('span.rateYDS::text').getall()
        tick_type = response.css('span.small.text-warm.pl-half span:nth-child(2) ::text').getall()
        tick_details = response.css('td.text-warm.small i ::text').getall()

        pagination = response.css('div.pagination a:nth-child(4) ::attr(href)').get()

        page_number = return_ele(stripped)

        route_id = []

        for i in user_ticks:
            route_id.append(strip_id(i))

        for item in zip(route_id, tick_type, tick_grades, tick_details):
            tick = tickData()
            tick['user_id'] = user_id
            tick['route_id'] = item[0]
            tick['route_type'] = item[1]
            tick['route_grade'] = item[2]
            tick['route_notes'] = item[3]

            yield tick

        if not pagination:
            return
        elif page_number >= self.page_max:
            return
        else:
            yield response.follow(url=pagination, callback=self.parse_user)


