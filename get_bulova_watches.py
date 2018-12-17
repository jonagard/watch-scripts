#!/usr/bin/env python

# This one uses the same backend as Citizen.  But the stopping condition is
# different.  With Citizen you get no 'product-tile' after you hit the end of
# the real pages in continual scroll.  Bulova still returns product-tiles even
# after you see all watches.  But it paginates so you can see what your current
# page is.  Once you see all watches, the current page doesn't move any more.
# We know we're done when we see a duplicate "current page".

import requests
from bs4 import BeautifulSoup as bs

preurl = "https://www.bulova.com/us/en/{}/?sz=12&start={}"

# 'watches-for-men' or 'womens', literal string
sex = 'watches-for-men'
#sex = 'womens'

start = 0
url = preurl.format(sex, start)
last_page = ''

while True:
    print(url)
    page = requests.get(url)
    soup = bs(page.text, 'html.parser')
    watch_tile = soup.find_all(class_='product-tile')
    page_class = soup.find(class_='current-page')
    current_page = page_class.get('title')
    if current_page == last_page:
        break

    last_page = current_page

    for item in watch_tile:
        filename = item.get('data-itemid')

        # have to pull out the specific 'img' class here because they have a
        # hover-over alt image named img-hover
        img_class = item.find(class_='img')
        img = img_class.find_all('img')
        try:
            response = requests.get('http:{}'.format(img[0].get('src')))
            with open('bulova_watches\\{}.png'.format(filename), 'wb') as f:
                f.write(response.content)
        except:
            print('Failed to get image for {}'.format(filename))

    start = start + 12
    url = preurl.format(sex, start)
