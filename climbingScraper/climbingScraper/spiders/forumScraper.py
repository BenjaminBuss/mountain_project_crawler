# ----------------------------
# scrapy scraper called mpScraper used to obtain tick information for specified area
#
# Benjamin Buss, www.github.com/BenjaminBuss
# ----------------------------

import scrapy
import re
from ..items import forumData

def strip_id(url):
    temp_regex = re.findall(r'\d+', url)
    temp_stripped = list(map(int, temp_regex))
    return temp_stripped

def return_ele(x):
    try:
        return x[1]
    except IndexError:
        return 1

def strip_year(x):
    return x.split(",").strip()

class ProjectSpider(scrapy.Spider):
    name = 'forumCrawler'
    allowed_domains = ['mountainproject.com']
    start_urls = ['https://www.mountainproject.com/forum']

    def parse(self, response):
        sub_links = response.css('a[href*=forum]::attr(href)').getall()

        for url in sub_links:
            thread_id = strip_id(url)
            if not thread_id:
                continue
            elif thread_id == 103989416:
                continue
            else:
                yield response.follow(url = url, callback = self.parse_sub)

    def parse_sub(self, response):
        forum_links = response.css('a[href*=forum\/topic]::attr(href)').getall()

        page_number = return_ele(strip_id(response.url))
        pagination = response.css('div.pagination a:nth-child(4) ::attr(href)').get()

        if not pagination:
            return
        elif page_number >= 50:
            return
        else:
            yield response.follow(url=pagination, callback=self.parse_sub)

        for url in forum_links:
            topic_id = strip_id(url)
            if not topic_id:
                continue
            else:
                yield response.follow(url =url, callback=self.parse_thread)

    def parse_thread(self, response):
        thread_id = strip_id(response.url)
        user_ids = response.css('table[id*=forum-table]  tr[id*=ForumMessage]::attr(data-user-id)').getall()
        mess_dates = response.css("a[class='permalink'] *::text").getall()
        pagination = response.css('div.pagination a:nth-child(4) ::attr(href)').get()

        for item in zip(user_ids, mess_dates):
            post = forumData()
            post['thread_id'] = thread_id[0]
            post['user_id'] = item[0]
            post['mess_date'] = item[1]
            yield post

        year = strip_year(mess_dates[-1])

        if not pagination:
            return
        elif year < 2020:
            return
        else:
            yield response.follow(url=pagination, callback = self.parse_thread)
