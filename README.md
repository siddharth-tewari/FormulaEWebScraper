# FormulaEWebScraper
Web scraper developed in Python that scrapes the official FIA Formula E website for driver/team standings and race informations and stores everything in JSON files.

## Required Python Packages

- requests
- os
- bs4
- docopt
- json

## How To Use

You can use this scraper withou any arguments. If you do so it will use it's default value (every season).

> python3 fescraper.py

### Arguments

The arguments for the scraper consist in the seasons you want to fetch. If you want a specific season, you just need to specify it like this:

> python3 fescraper.py 2018/2019

If you want to scrape multiple seasons you can use it the following way.

> python3 fescraper.py 2017/2018 2019/2020 2018/2019

The order in which you specify the arguments does not affect the final result. It only changes the order in which the information is fetched.