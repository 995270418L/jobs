# 爬取所有地名的（城市名）

import requests
import logging
from lagou.domain.CityModel import CityModel
import uuid
import re
from lagou.common_s import constants
from bs4 import BeautifulSoup
logger = logging.getLogger(__name__)

# 获取拉钩网所有城市信息
def update_city_info():
    response = requests.get(constants.ALL_CITY_URL).text
    html = BeautifulSoup(response,'lxml')
    city_list = html.select('.city_list a')
    city_model_list = []
    for city_info in city_list:
        city_name = ''.join(city_info.stripped_strings)
        city_id = city_info['href']
        city_id = re.findall(pattern=r'/(\d+)-\d+-\d+$', string=city_id)[0]
        city = CityModel(id=str(uuid.uuid1()),city_id=city_id,city_name=city_name,city_source='拉勾')
        city_model_list.append(city)
    CityModel.add_all(cities = city_model_list)
