# ----------------------------
# scrapy scraper called mpScraper used to obtain tick information for specified user
#
# Benjamin Buss, www.github.com/BenjaminBuss
# ----------------------------

import scrapy
import re
from ..items import userData
import boto3
from pandas import read_csv

# Functions
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
    name = 'userScraper'
    allowed_domains = ['mountainproject.com']

    # Connect to S3 bucket
    client = boto3.client('s3')
    resource = boto3.resource('s3')
    my_bucket = resource.Bucket('mpcrawlerdump')
    obj = client.get_object(Bucket = 'mpcrawlerdump', Key = 'forumCrawler/tidyied/user_urls.csv')
    grid_sizes = read_csv(obj['Body'])

    start_urls = [url.strip() for url in grid_sizes['url']]

    def parse(self, response):
        url = response.url
        url = url + '/ticks'
        yield response.follow(url = url, callback = self.parse_user)

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
            tick = userData()
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
        elif page_number >= 10:
            return
        else:
            yield response.follow(url=pagination, callback=self.parse_user)
