"""Web scraper developed in Python that scrapes the official FIA Formula E website for driver/team standings and race informations and stores everything in JSON files.\n
Usage:
  fescraper.py [<year>]...
  fescraper.py --version
  fescraper.py (-h | --help)

Try: fescraper.py
     fescraper.py 2019/2020
     fescraper.py 2017/2018 2018/2019 2019/2020 2020/2021 2021/2022

Options:
  -h --help            show this help message and exit
  --version            show version and exit
"""

import requests
import race
import os
from bs4 import BeautifulSoup
from docopt import docopt

def discoverSeason(year):
    if year == "2014/2015":
        return str(1)
    elif year == "2015/2016":
        return str(2)
    elif year == "2016/2017":
        return str(3)
    elif year == "2017/2018":
        return str(4)
    elif year == "2018/2019":
        return str(5)
    elif year == "2019/2020":
        return str(6)
    elif year == "2020/2021":
        return str(7)
    elif year == "2021/2022":
        
    else:
        return str(0)


def start(years):
    for i in range(len(years)):

        season = discoverSeason(years[i])
        year = years[i]

        if season == str(0):
            return 0
        else :
            folder = "Season " + season

            if not os.path.exists(folder):
                os.makedirs(folder)

            fyear = year.split('/', 1)[0]

            print("> Scraping " + year + " season")

            baseurl = "https://www.fiaformulae.com/results/race-results/?championship=202" + fyear

            page = requests.get(baseurl)
            soup = BeautifulSoup(page.content, features="html.parser")

            i = 1;

            for element in soup.find('select', class_='js-select-change-race').find_all('option'):
                url = "https://www.fiaformulae.com/results/race-results/?championship=202" + fyear + "&race=" + element['value']
                race.scrape(url,folder,i)
                i = i+1

if __name__ == '__main__':
    arguments = docopt(__doc__, version='FE Web Scraper 1.0')
    args = arguments.get("<year>")

    r = 1

    if len(args) == 0:
        years = ["2014/2015", "2015/2016", "2016/2017", "2017/2018", "2018/2019", "2019/2020", "2020/2021", "2021/2022"]
        r = start(years)
    elif len(args) > 0:
        years = args
        r = start(years)

    if r == 0:
        print("> Invalid arguments")


