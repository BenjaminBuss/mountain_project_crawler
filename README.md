
# Mountain Project Tick Scraper

Have you ever wanted a near unending amount of very niche data? Do you want to feel bad about pulling all this data from a site that provides a quality service for free? Well I have just the script for you. 

You can check out Mountain Project [here](https://www.mountainproject.com/). And MPs terms of service [here](https://www.adventureprojects.net/ap-terms). For a more legimiate an possibly simplier method you can see the documentation for Mountain Project's API [here](https://www.mountainproject.com/data).


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

This scraper is designed for you to be able to scrape several pieces of data from any Mountain Project Area, and export it to an AWS S3 bucket.

1. All of the routes contained that area(or it's subareas), and basic information like route name, grade, stars, shared date, MP identifier, and more are returned.
2. All of the ticks for each of those routes, and the users who ticked them.
3. All of those users other ticks, up to a pre-specified number of previous ticks.

Originally I had hoped to upload the three pieces of data into three separate folders in the S3 bucket but I was too dumb to figure out how to change the feed uri of S3 buckets in an item pipeline. So the data instead dumps all three pieces into a series of jumbled json files.


**Example:** 

Area to Scrape: 

`https://www.mountainproject.com/area/113250571/watch-tower-boulder`

Returned data:
```
{'id': 'route', 'route_id': 113250669, 'route_name': 'Pending Approval', 'route_grade': 'V2', 'route_stars': 'Avg: 3.8 from 4 votes', 'route_type': 'Boulder, 30ft(9m)', 'route_fa': 'unknown', 'route_views': '496 total, 12/month', 'route_share': 'July 3, 2017'}
{'id': 'tick', 'route_id': 113250669, 'user_id': 7040154}
{'id': 'usti', 'route_id': 109593707, 'user_id': 7040154, 'route_type': 'Boulder', 'route_grade': 'V6-', 'route_notes': 'Nov 26, 2017', 'route_name': 'The Round Room'} 
{'id': 'usti', 'route_id': 113250669, 'user_id': 7040154, 'route_type': 'Boulder', 'route_grade': 'V2' , 'route_notes': 'Jul 11, 2017', 'route_name': 'Pending Approval'}
```


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

This spider is historically run on an Amazon AWS t2.micro EC2 instance, with the data being dumped into a S3 bucket, however you can run it on local machine and have it export locally as well.

After you've clone the repository, navigate to the project directory and run it. When running the mpScraper spider you have two possible arguments.

* Domain: *string*, **required**, the initial URL of the area to scrape(typically you'd want the URL to be an area, but if you scrape a single route it will still work as intended).
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

Three different scrapy items are returned through the running of the script:

1. **Route Data**

Name | Type | Description
---- | ---- | -----------
id | *string* | Used to identify the json
route_id | *int* | Numerical identifier for the route pulled from the Mountain Project URL.
route_name | *string* | The routes name.
route_grade | *string* | The routes YDS or V-scale grade.
route_stars | *string* | The number of stars(out of four), and opinions that lead to that rating.
route_type | *string* | The type(Boulder, Sport, Trad, Alpine).
route_fa | *string* | The first ascensionists name.
route_views | *string* | The number of total views and views per week/month/year.
route_share | *string* | The date the route was originally shared.

2. **User Ticks**

Name | Type | Description
---- | ---- | -----------
id | *string* | Used to identify the json
user_id | *int* | Numerical identifier for the user pulled from the MP URL.
route_id | *int* | Numerical identifier for the route pulled from the MP URL.

3. **Tick Data**

Name | Type | Description
---- | ---- | -----------
id | *string* | Used to identify the json
user_id | *int* | Numerical identifier for the user pulled from the MP URL.
route_id | *int* | Numerical identifier for the route pulled from MP URL.
route_type | *string* | Type(Boulder, Sport, Trad, Alpine).
route_grade | *string* | The routes YDS or V-scale grade.
route_notes | *string* | Any notes about send type(flash, onsight, attempt) as well as any additional information users provided.
route_name | *string* | The name of the route.


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
