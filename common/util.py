# 通用爬虫工具类
import time
import random
from common import constants

def crawl_sleep():
    time.sleep(random.uniform(constants.MIN_SLEEP_TIME, constants.MAX_SLEEP_TIME))
