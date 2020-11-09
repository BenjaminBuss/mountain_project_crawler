# Mountain Project Tick Scraper

Have you ever wanted a near unending amount of very niche data? Do you want to feel bad about pulling all this data from a site that provides a quality service for free? Well, I have just the script for you. This poorly made scraper is designed to take a mountain project area(E.g `https://www.mountainproject.com/area/105716826/saint-george`), and scrape all areas and subareas. Then parse and yield some basic route data, before finally, pulling all ticks for each area and parsing out all of their previous ticks.

## Table of Contents

* [About the Project](#about-the-project)
* [Getting Started](#getting-started)
  * [Prerequisites](#prerequisites)
  * [Installation](#installation)
* [Usage](#usage)
  * [Data Format](#data-format)
* [Roadmap](#roadmap)
* [Contributing](#contributing)
* [License](#license)
* [Contact](#contact)
* [Acknowledgements](#acknowledgements)




## About The Project


## Getting Started

To get a local copy up and running follow these simple steps.

### Prerequisites

This is an example of how to list things you need to use the software and how to install them.
* npm
```sh
npm install npm@latest -g
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



<!-- USAGE EXAMPLES -->
## Usage

Use this space to show useful examples of how a project can be used. Additional screenshots, code examples and demos work well in this space. You may also link to more resources.

Before running the script, you need to set the `FEED` to your prefered export method. An Amazon S3 Bucket was originally used. For more information on Feed Exports check out the Scrapy documentation [here](https://docs.scrapy.org/en/latest/topics/feed-exports.html). 


### Data Format

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





# All of this may go unused

<!-- ROADMAP -->
## Roadmap

See the [open issues](https://github.com/github_username/repo_name/issues) for a list of proposed features (and known issues).



<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE` for more information.



<!-- CONTACT -->
## Contact

Your Name - [@twitter_handle](https://twitter.com/twitter_handle) - email

Project Link: [https://github.com/github_username/repo_name](https://github.com/github_username/repo_name)


