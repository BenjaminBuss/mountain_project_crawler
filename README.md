
# Mountain Project Tick Scraper

You can check out Mountain Project [here](https://www.mountainproject.com/). And MPs terms of service [here](https://www.adventureprojects.net/ap-terms). For a more legitimate an possibly simpler method you can see the documentation for Mountain Project's API [here](https://www.mountainproject.com/data).

Have you ever wanted a near unending amount of very niche data? Do you want to feel bad about pulling all this data from a site that provides a quality service for free? Well I have just the script for you. This repository contains a series of Scrapy spiders and scripts to scrape forum posts, users , and tick data. The data received is used to poke fun at the gumbys who post on the Mountain Project forums.


## Table of Contents

* [About the Project](#about-the-project)
* [Getting Started](#getting-started)
  * [Prerequisites](#prerequisites)
  * [Installation](#installation)
* [Usage](#usage)
  * [Spiders](#spiders)
  * [Scripts](#scripts)
* [Roadmap](#roadmap)
* [Contributing](#contributing)
* [License](#license)
* [Contact](#contact)


## About The Project

This scraper is designed for you to be able to scrape enough data for you to try and make fun of the posters on the Mountain Project forums. 

The two main pieces of data scraped are: 

1. All of the forum posts for 2020, who posted them, and when.

2. A pre-specified number of ticks for all the users who at one point or another posted on the forums.

Yeah, you can probably see where this is going.


## Getting Started

To get a local copy up and running follow these steps.


### Prerequisites

* python3
* scrapy
* botocore
* python-dotenv

```sh
sudo apt-get install python3 python3-dev python3-pip libxml2-dev libxslt1-dev zlib1g-dev libffi-dev libssl-dev git
```


### Installation

1. Clone the repo
```sh
git clone https://github.com/BenjaminBuss/mountain_project_crawler.git
```

2. Install additional Python packages
```sh
pip3 install scrapy botocore python-dotenv
```

Botocore is required for using S3 for more information you can check out the repository [here](https://github.com/boto/botocore). Additionally, `python-dotenv` is used in setting.py to provide a rudimentary level of security to the AWS credentials. For more information and a walk through on how to use it check out the repository [here](https://github.com/theskumar/python-dotenv).

To set up your AWS credentials you need to create a `.env` file in the same level as `setting.py`. You can create a `.env` file with the following command:
```
touch .env
nano .env
```

Then in this file you just need to add the following two lines, obviously replacing `ACCESS_KEY` AND `SECRET_KEY` with their respective values.
```
AWS_ACCESS_KEY_ID =  [ACCESS_KEY]
AWS_SECRET_ACCESS_KEY = [SECRET_KEY]
```

After adding in the credentials you need to updated the bucket name in all three places in the `FEEDS` argument of `settings.py` from *mpcrawlerdump* to your buckets name. And specify the bucket region in `AWS_REGION_NAME`.


## Usage

These spiders and scripts were historically run on an Amazon AWS t2.micro EC2 instance, with the data being dumped into a S3 bucket, however you can run it on local machine and have it export locally as well(With some adjustments to a few of the spiders and scripts). Both of the AWS services used are free for the first 12 months of use.

After you've clone the repository, navigate to the project directory and run it.


### Spiders


#### forumScraper

**Arguments:** None.

**Example Usage:**
```
scrapy crawl forumScraper
```

**Default Scraping Parameters:** All forum posts from 2020 within the first 50 pages of a post with the except of any posts in the 'For Sale' section.

**Data Returned:** 

Name | Type | Description
---- | ---- | -----------
thread_id | *string* | Used to identify the thread the post was in.
user_id | *int* | Unique identifier of the user.
mess_date | *date* | The date the message was posted.


#### userScraper

**Arguments:** Pages(default 10), the number of pages to scrape from each user.

**Example Usage:**
```
scrapy crawl userScraper -a pages=20
```

**Default Scraping Parameters:** Scrapes from the dataset created after running the forumScraper spider and the `get_forum_posts` script.

**Data Returned:** user_id, route_id, route_type, route_grade, route_notes.

Name | Type | Description
---- | ---- | -----------
user_id | *int* | Numerical identifier for the user pulled from the MP URL.
route_id | *int* | Numerical identifier for the route pulled from MP URL.
route_type | *string* | Type(Boulder, Sport, Trad, Alpine).
route_grade | *string* | The routes YDS or V-scale grade.
route_notes | *string* | Any notes about send type(flash, onsight, attempt) as well as any additional information users provided.
route_name | *string* | The name of the route.


For more documentation on executing scrapy spiders check out the documentation [here](https://docs.scrapy.org/en/latest/topics/commands.html). For more details on spider arguments you can find the documentation [here](https://docs.scrapy.org/en/latest/topics/spiders.html#spider-arguments).


### Scripts

#### get_forum_posts

A simple python script meant to be run after you run the forumScraper spider and before you run the userScraper spider. It does two things: 

1. Create a dataset of how many times each user posted.

2. Created a series of links to all the users who posted to input into the userScraper spider.


#### create_user_profile

XYZ


## Roadmap

See the [open issues](https://github.com/benjaminbuss/mountain_project_crawler/issues) for a list of proposed features (and known issues).


## Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request


## License

Distributed under the MIT License. See `LICENSE` for more information.


## Contact

Benjamin Buss - [@twitter_handle](https://twitter.com/twitter_handle) - email

Project Link: [https://github.com/benjaminbuss/mountain_project_crawler](https://github.com/BenjaminBuss/mountain_project_crawler)
