# Mountain Project Tick Scraper

Have you ever wanted a near unending amount of very niche data? Do you want to feel bad about pulling all this data from a site that provides a quality service for free? Well I have just the script for you. 


## Table of Contents

* [About the Project](#about-the-project)
* [Getting Started](#getting-started)
  * [Prerequisites](#prerequisites)
  * [Installation](#installation)
* [Usage](#usage)
  * [Data Format](#yielded-data-formatting)
* [Roadmap](#roadmap)
* [Contributing](#contributing)
* [License](#license)
* [Contact](#contact)


## About The Project

This scraper is designed for you to be able to scrape two main pieces of data from any Mountain Project Area, such as [St. George](https://www.mountainproject.com/area/105716826/saint-george), and export it to an AWS S3 bucket.

1. All of the routes contained that area(or it's subareas), and basic information like route name, grade, and MP identifier are returned(*I want to add more info into this, stars, shared data, area/sub-area information etc*)
2. All of the ticks for each of those routes, and the users who ticked them.
3. All of those users other ticks, up to a pre-specified number of previous ticks.

It's currently not the most efficient and missing some nice pieces of information, but hopefully it'll

**E.G.** https://www.mountainproject.com/area/113250571/watch-tower-boulder

Returned data:
```
routeData = { route_id = 113250669, route_name = 'Pending Approval', route_grade = 'V2' }

userTicks = { route_id = 113250669, user_id = 7040154 }

tickData  = { route_id = 109593707, user_id = 7040154, route_type = Boulder, route_grade = 'V6-', route_notes = 'Nov 26, 2017' }, 

   { route_id = 113250669, user_id = 7040154, route_type = Boulder, route_grade = 'V2' , route_notes = 'Jul 11, 2017' }
```



## Getting Started

To get a local copy up and running follow these simple steps.


### Prerequisites


* python3
* scrapy
* botocore
* python-dotenv

```sh
sudo apt-get install python3 python3-dev python-pip libxml2-dev libxslt1-dev zlib1g-dev libffi-dev libssl-dev
```


### Installation

1. Clone the repo
```sh
git clone https://github.com/BenjaminBuss/mountain_project_crawler.git
```
2. Install additional Python packages
```sh
pip install scrapy botocore python-dotenv
```

Botocore is required for using S3 for more information you can check out the repository [here](https://github.com/boto/botocore)

Additionally, `python-dotenv` is used in setting.py to provide a rudimentary level of security to the AWS credentials. For more information and a walk through on how to use it check out the repository [here](https://github.com/theskumar/python-dotenv).

To set up your AWS credentials you need to create a `.env` file in the same level as `setting.py`, in this file you just need to add the following two lines, obviously replacing `ACCESS_KEY` AND `SECRET_KEY` with their respective values.

```
AWS_ACCESS_KEY_ID =  [ACCESS_KEY]
AWS_SECRET_ACCESS_KEY = [SECRET_KEY]
```

After adding in the credentials you need to updated the bucket name in all three places in the `FEEDS` argument of `settings.py` from *mpcrawlerdump* to your buckets name.


## Usage

Before running the script, you need to set the `FEED` to your preferred export method. An Amazon S3 Bucket was originally used. For more information on Feed Exports check out the Scrapy documentation [here](https://docs.scrapy.org/en/latest/topics/feed-exports.html), alternatively the [Data Format](#yielded-data-formatting) subsection has more information on what data is returned and how it is meant to be handled/stored.

After the feeds have been specified, you can navigate to the project directory and run it. When running the mpScraper spider you have two possible arguments.

* Domain: *string*, **required**, the initial URL of the area to scrape.
    * EG: https://www.mountainproject.com/area/118272520/wales-canyon
* Pages: *int, default 10*, the number of pages of user ticks to scrape(per user).

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

Two different scrapy items are returned through the running of the script:

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


## Roadmap

Until I figure out how this open issues things works I'm going to keep a light list here

* Add more data to route information
    * Stars, shared date, route type, height, comments, site activity, etc.
* Add ability to scrape more user data(forum posts)


See the [open issues](https://github.com/benjaminbuss/mountain_project_crawler/issues) for a list of proposed features (and known issues).


https://github.com/aivarsk/scrapy-proxies



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

Your Name - [@twitter_handle](https://twitter.com/twitter_handle) - email

Project Link: [https://github.com/benjaminbuss/mountain_project_crawler](https://github.com/benjaminbuss/mountain_project_crawler)




