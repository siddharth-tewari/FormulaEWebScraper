# Race Results Module

import requests
import json
from bs4 import BeautifulSoup

def createFilename(season,race):
    frag = season.split()
    filename = str("S") + frag[1] + str("_R") + str(race)
    return filename


def scrape(url,folder,number):
    # print("> Accessing: "+url)
    data = {}

    page = requests.get(url)
    encoding = page.encoding if 'charset' in page.headers.get('content-type', '').lower() else None

    soup = BeautifulSoup(page.content, features="html.parser", from_encoding=encoding)

    event = soup.find_all('option', {'selected': True})
    drivers = soup.find_all('tr', class_='table__row')
    month = soup.find('span', class_='race-info__date-month').text
    day = soup.find('span', class_='race-info__date-day').text

    data['season'] = event[0].text
    data['race'] = event[1].text
    data['round'] = number
    data['date'] = month + str(" ") + day

    filename = createFilename(event[0].text,number)

    if soup.find('h1', class_='standings-intro__title') != None:
        if soup.find('h1', class_='standings-intro__title').text == "E-Prix":

            data['e-prix'] = []
            for driver in drivers:
                position = driver.find('div', class_='pos').find('span', class_='value').text
                firstname = driver.find('div', class_='driver__fname').text
                lastname = driver.find('div', class_='driver__lname').find('span', class_='full').text
                number = driver.find('div', class_='driver__number').text
                team = driver.find('div', class_='team').find('span', class_='team__name').text
                started = driver.find('td', class_='td-started td-stat show-at-tablet-portrait').find('span', class_='stat__value').text
                best = driver.find('td', class_='td-best td-stat show-at-tablet-portrait').find('span', class_='stat__value').text
                time = driver.find('td', class_='td-time td-stat').find('span', class_='stat__value').text
                points = driver.find('td', class_='td-points').find('div', class_='points').text

                if time == "–":
                    time = "DNF"

                data['e-prix'].append({
                    'position': position,
                    'driver': firstname + str(" ") + lastname,
                    'number': number,
                    'team': team,
                    'started': started,
                    'best': best,
                    'time': time,
                    'points': points
                })

    urlqsuper = url + "&session=SuperPoleResults"

    # print("> Accessing: " + urlqsuper)

    page = requests.get(urlqsuper)
    encoding = page.encoding if 'charset' in page.headers.get('content-type', '').lower() else None

    soup = BeautifulSoup(page.content, features="html.parser", from_encoding=encoding)

    drivers = soup.find_all('tr', class_='table__row')

    if soup.find('h1', class_='standings-intro__title') != None:
        if soup.find('h1', class_='standings-intro__title').text == "Super Pole":

            data['super pole'] = []
            for driver in drivers:
                position = driver.find('div', class_='pos').find('span', class_='value').text
                firstname = driver.find('div', class_='driver__fname').text
                lastname = driver.find('div', class_='driver__lname').find('span', class_='full').text
                number = driver.find('div', class_='driver__number').text
                team = driver.find('div', class_='team').find('span', class_='team__name').text
                time = driver.find('td', class_='td-time td-stat').find('span', class_='stat__value').text

                data['super pole'].append({
                    'position': position,
                    'driver': firstname + str(" ") + lastname,
                    'number': number,
                    'team': team,
                    'time': time,
                })

    urlquali = url + "&session=QualifyingPracticeAll"

    # print("> Accessing: "+urlquali)

    page = requests.get(urlquali)
    encoding = page.encoding if 'charset' in page.headers.get('content-type', '').lower() else None

    soup = BeautifulSoup(page.content, features="html.parser", from_encoding=encoding)

    drivers = soup.find_all('tr', class_='table__row')


    if soup.find('h1', class_='standings-intro__title') != None:
        if soup.find('h1', class_='standings-intro__title').text == "Qualification":

            data['qualification'] = []
            for driver in drivers:
                position = driver.find('div', class_='pos').find('span', class_='value').text
                firstname = driver.find('div', class_='driver__fname').text
                lastname = driver.find('div', class_='driver__lname').find('span', class_='full').text
                number = driver.find('div', class_='driver__number').text
                team = driver.find('div', class_='team').find('span', class_='team__name').text
                time = driver.find('td', class_='td-time td-stat').find('span', class_='stat__value').text

                data['qualification'].append({
                    'position': position,
                    'driver': firstname + str(" ") + lastname,
                    'number': number,
                    'team': team,
                    'time': time,
                })


    with open(folder+'/%s.json' % filename, "w") as outfile:
        json.dump(data, outfile, indent=4, ensure_ascii=False)

    print("> Dumped " + '%s.json' % filename)
