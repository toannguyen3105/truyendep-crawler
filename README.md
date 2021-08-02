Crawl data website truyendep.com using Scrapy (https://crawl.toannguyen3105.com/)
=======================================================
Use Scrapy to crawl the website Truyendep.com

Prerequisites
--------
Before you continue, ensure you meet the following requirements:

* You have installed the latest version of Ruby.
* You are using a Windows, Linux or Mac OS machine.
* You have a basic understanding of Python, Scrapy.
* Get your proxy list from sites like https://vietpn.com/ (copy-paste into text file and 
  reformat to http://username:password@host:port format)
  
Install
--------
* You should use the virtual environment to run the program and install the library via the pip command
> pip install -r requirements.txt
* Create a *.env* file in the root directory of your project where you declare the PROXY_PATH environment variable pointing to the file containing the proxy list
> PROXY_PATH=/home/user/proxies.txt

Usage
--------
* Run the command below to get all story data
>  scrapy crawl comics -O truyendep_scifi.csv
* Run the command below to get "Sci fi" category
>  scrapy crawl comics -a category="Sci fi" -O truyendep_scifi.csv

Data sample
--------
### Data was crawl at 2021-08-01

Full data
> [Truyendep.com Full Comic](https://drive.google.com/file/d/1nj-XQ0Zh4qf23Cy4FoPDxZE5bYtfjNGj/view?usp=sharing)

Scifi Category
> [Truyendep.com Scifi Category](https://drive.google.com/file/d/1AzO6cb9N8tL6CboLg6JO0lZiqe7bg3iX/view?usp=sharing)