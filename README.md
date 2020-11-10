# Mountain Project Tick Scraper

Have you ever wanted a near unending amount of very niche data? Do you want to feel bad about pulling all this data from a site that provides a quality service for free? Well, I have just the script for you. 

This poorly made scraper is designed to take a mountain project area(E.g `https://www.mountainproject.com/area/105716826/saint-george`), and scrape all areas and subareas. Then parse and yield some basic route data, before finally, pulling all ticks for each route, and parsing out all of the users previous ticks.

## Table of Contents

* [About the Project](#about-the-project)
* [Getting Started](#getting-started)
  * [Prerequisites](#prerequisites)
  * [Installation](#installation)
* [Usage](#usage)
  * [Data Format](#yielded-data-formatting)


## About The Project


## Getting Started

To get a local copy up and running follow these simple steps.

### Prerequisites

This is an example of how to list things you need to use the software and how to install them.
* npm
```sh
sudo apt-get install python3 python3-dev python-pip libxml2-dev libxslt1-dev zlib1g-dev libffi-dev libssl-dev
```

### Installation

1. Clone the repo
```sh
git clone https://github.com/BenjaminBuss/mountain_project_scraper.git
```
2. Install NPM packages
```sh
npm install
```

https://github.com/aivarsk/scrapy-proxies


## Usage

Before running the script, you need to set the `FEED` to your preferred export method. An Amazon S3 Bucket was originally used. For more information on Feed Exports check out the Scrapy documentation [here](https://docs.scrapy.org/en/latest/topics/feed-exports.html). 

After specifying the initial data feeds the scraper is run like any other scrapy spider. You navigate to the projects directory

When running the mpScraper spider you have two possible arguments.

* Domain: string, *required*, the initial URL of the area to scrape.
    * EG: https://www.mountainproject.com/area/118272520/wales-canyon
* Pages: int, default 10, the number of pages of user ticks to scrape(per user).

Example of scraping the Wales Canyon area:
```
scrapy crawl mpScraper -a domain='https://www.mountainproject.com/area/118272520/wales-canyon'
```

Example using the pages argument to limit the number of pages you scrape to save time and server load.
```
scrapy crawl mpScraper -a domain='https://www.mountainproject.com/area/118272520/wales-canyon' -a pages=2
```

For more documentation on executing scrapy spiders check out the documentation [here](https://docs.scrapy.org/en/latest/topics/commands.html). For more details on spider arguments you can find the documentation [here](https://docs.scrapy.org/en/latest/topics/spiders.html#spider-arguments).


### Yielded Data Formatting 

Three different scrapy items are returned through the running of the script:

1. **Route Data**

Name | Type | Description
---- | ---- | -----------
route_id | *int* | Numerical identifier for the route pulled from the Mountain Project URL.
route_name | *string* | The routes name.
route_grade | *string* | The routes YDS or V-scale grade.


2. **Tick Data**

Name | Type | Description
---- | ---- | -----------
user_id | *int* | Numerical identifier for the user pulled from the MP URL.
route_id | *int* | Numerical identifier for the route pulled from MP URL.
route_type | *string* | Type(Boulder, Sport, Trad, Alpine).
route_grade | *string* | The routes YDS or V-scale grade.
route_notes | *string* | Any notes about send type(flash, onsight, attempt) as well as any additional information users provided.


3. **Route Ticks**

