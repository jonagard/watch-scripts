#!/usr/bin/env python

import requests
from bs4 import BeautifulSoup as bs

# 2 = men
# 1 = women
sex = 1

# The unit field just has to be larger than how many total watches they have.
# At the time of this writing, they had 191 men's watches
page = requests.get('https://www.seikowatches.com/__api/posts/list?category_id=11137&custom_field__sex_web_search={}&paginate=true&unit=200'.format(sex))
watches = page.json()

for item in watches['results']:
    filename = item['thumbnail']['file_name']
    url = 'https://storage.seikowatches.com/production/images' + item['thumbnail']['url_key'] + '_medium.png'
    try:
        response = requests.get(url)
        with open('seiko_watches\\{}.png'.format(filename), 'wb') as f:
            f.write(response.content)
    except:
        print('Failed to get image for {}'.format(filename))
