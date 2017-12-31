import requests
import re
from bs4 import BeautifulSoup

url = 'https://www.lagou.com/gongsi/allCity.html?option=0-0-0'

text = requests.get(url).text
html = BeautifulSoup(text,'lxml')
tags = html.select('.city_list a')
for tag in tags:
    print(tag)
    city_name = ''.join(tag.stripped_strings)
    city_id = tag['href']
    city_id = re.findall(pattern = r'/(\d+)-\d+-\d+$',string=city_id)[0]