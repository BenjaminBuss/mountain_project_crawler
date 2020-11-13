# ----------------------------
# scrapy scraper called mpScraper used to obtain tick information for specified area
#
# Benjamin Buss, www.github.com/BenjaminBuss
# ----------------------------

import scrapy
import re
from ..items import tickData, routeData, userTicks

def strip_id(url):
    temp_regex = re.findall(r'\d+', url)
    temp_stripped = list(map(int, temp_regex))
    return temp_stripped

def return_ele(x):
    try:
        return x[1]
    except IndexError:
        return 1

class ProjectSpider(scrapy.Spider):
    name = 'mpScraper'
    allowed_domains = ['mountainproject.com']

    def __init__(self, domain='', pages='10', *args, **kwargs):
        # Provides ability to specify start URL from the command line.
        super(ProjectSpider, self).__init__(*args, **kwargs)
        self.start_urls = [f'{domain}']
        self.page_max = int(f'{pages}')

    def parse(self, response):
        # Parses original start area and iterates through all sub areas
        area_link = response.css('div.mp-sidebar a[href*=area]::attr(href)').getall()

        if len(area_link) <= 0:
            # if there are no subareas, iterate through routes
            route_link = response.css('div.mp-sidebar a[href*=route]::attr(href)').getall()
            for url in route_link:
                yield response.follow(url=url, callback=self.parse_routes)
        else:
            # Iterate through subarea urls, add to an array, send them to be parsed
            for url in area_link:
                yield response.follow(url=url, callback=self.parse)

    def parse_routes(self, response):
        # Parses route information and checks users ticks
        route_name = response.css('div.col-md-9.float-md-right.mb-1 h1::text').get().strip()
        route_grade = response.css("span.rateYDS::text").get()
        route_stars = response.css("[id*='starsWithAvgText']::text").getall()[1].strip()
        route_addinfo = [item.strip() for item in response.css("table[class='description-details'] > tr > td::text").getall()]
        route_type = route_addinfo[1]
        route_fa = route_addinfo[3]
        route_views = route_addinfo[5]
        route_date = route_addinfo[8]

        route_subinfo = response.css('a.show-tooltip ::attr(href)').get()
        route_id = int(strip_id(route_subinfo)[0])

        route_info = routeData()
        route_info['id_route'] = route_id
        route_info['name_route'] = route_name
        route_info['grade_route'] = route_grade
        route_info['stars_route'] = route_stars
        route_info['type_route'] = route_type
        route_info['fa_route'] = route_fa
        route_info['views_route'] = route_views
        route_info['date_route'] = route_date

        yield route_info
        yield response.follow(url=route_subinfo, callback=self.get_users)

    def get_users(self, response):
        # Correlates ticks / route_id to user_id
        route_id = strip_id(response.url)
        route_ticks = response.css('.col-lg-6  a[href*=user]::attr(href)').getall()

        for url in route_ticks:
            tick_url = url + '/ticks'
            user_id = strip_id(url)

            ticks = userTicks()
            ticks['user'] = user_id[0]
            ticks['route'] = route_id[0]

            yield ticks
            yield response.follow(url=tick_url, callback=self.parse_user)

    def parse_user(self, response):
        # Parses through users previous ticks
        stripped = strip_id(response.url)
        user_id = stripped[0]  # strip_id returns two numbers, ID and page number, this gets just ID
        page_number = return_ele(stripped)  # just gets page number

        user_ticks = response.css('a[href*=route]::attr(href)').getall()
        tick_names = response.css("[class*='route-table'] a[href*=route] >strong *::text").getall()
        tick_grades = response.css('span.rateYDS::text').getall()
        tick_type = response.css('span.small.text-warm.pl-half span:nth-child(2) ::text').getall()
        tick_details = response.css('td.text-warm.small i ::text').getall()
        pagination = response.css('div.pagination a:nth-child(4) ::attr(href)').get()

        route_id = []
        for i in user_ticks:
            # Strip ID out of URLs for yielding
            tick_id = strip_id(i)

            if not tick_id:
                # Check to make sure there is a actual ID
                # For cases like: https://www.mountainproject.com/route-guide
                continue
            else:
                route_id.append(tick_id[0])

        for item in zip(route_id, tick_type, tick_grades, tick_details, tick_names):
            tick = tickData()
            tick['user_id'] = user_id
            tick['route_id'] = item[0]
            tick['route_type'] = item[1]
            tick['route_grade'] = item[2]
            tick['route_notes'] = item[3]
            tick['route_name'] = item[4]

            yield tick

        # Logic to prevent errors when at end of users pages or
        #       to stop if reached max number of pages
        if not pagination:
            return
        elif page_number >= self.page_max:
            return
        else:
            yield response.follow(url=pagination, callback=self.parse_user)
