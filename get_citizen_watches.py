#!/usr/bin/env python

import requests
from bs4 import BeautifulSoup as bs

preurl = "https://www.citizenwatch.com/us/en/{}/?sz=24&start={}&format=page-element"
# 'mens' or 'ladies', literal string
sex = 'mens'

start = 0
url = preurl.format(sex, start)

while True:
    page = requests.get(url)
    soup = bs(page.text, 'html.parser')
    watch_tile = soup.find_all(class_='product-tile')
    if not watch_tile:
        break
    for item in watch_tile:
        filename = item.get('data-itemid')
        img = item.find_all('img')
        try:
            response = requests.get('http:{}'.format(img[0].get('src')))
            with open('citizen_watches\\{}.png'.format(filename), 'wb') as f:
                f.write(response.content)
        except:
            print('Failed to get image for {}'.format(filename))

    start = start + 24
    url = preurl.format(sex, start)
