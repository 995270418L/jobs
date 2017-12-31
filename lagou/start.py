
import logging.config

import asyncio
from lagou.tasks import company
import time
from lagou.domain.CityModel import CityModel
from lagou.common_s import constants
from common.db import redis_instance
logger = logging.getLogger(__name__)
import threading

def main():
    while True:
        url = redis_instance.lpop(constants.DIS_QUEUE)
        # url = 'https://www.lagou.com/gongsi/153-1-27.json'
        if isinstance(url, bytes):
            url = url.decode('utf8')
        if url:
            start = time.time()
            logger.info("正在爬取url: {},开始时间:{}".format(url,start))
            company.distribute(url)
            end = time.time()
            logger.info("爬取任务结束，共耗时:{}".format(end-start))
        else:
            logger.info('任务已经完成。再见！')
            break

def distribute_lagou():
    # 首先删除redis里面所有的地址信息
    redis_instance.delete(constants.DIS_QUEUE)
    cities = CityModel.gat_all()
    for city in cities:
        city_id = city.city_id
        for i in constants.FINANCE_STAGE_DICT:
            for j in constants.INDUSTRY_FIELD:
                url = constants.CITY_COMPANY_URL.format(city_id,constants.FINANCE_STAGE_DICT[i],constants.INDUSTRY_FIELD[j])
                logger.info('正在爬取城市:{0}，融资阶段:{1}，行业领域为:{2}的公司页面'.format(str(city.city_name), str(i), str(j)))
                redis_instance.rpush(constants.DIS_QUEUE,url)

# 协程 demo 实现(生成器)
def consumer():
    print('Init consumer')
    r = 'init ok'
    while True:
        n = yield r
        print('consumer n={0} r={1}'.format(n,r))
        r = 'comsumer {} OK'.format(n)
def producer(c):
    print('Init producer')
    r = c.send(None)
    print('Start consumer, return {}'.format(r))
    n = 0
    while n < 5:
        n += 1
        print('While,Producer {}'.format(n))
        r = c.send(n)
        print('consume return {}'.format(r))
    c.close()
    print('close producer')

# 异步IO实现(asyncio)
@asyncio.coroutine
def tasks_asyncio(index):
    print("hello world, index:{0},thread:{1}".format(index,threading.current_thread()))
    yield from asyncio.sleep(1)
    print("hello world, index:{0},thread:{1}".format(index,threading.current_thread()))

def test():
    loop = asyncio.get_event_loop()
    tasks = [tasks_asyncio(1),tasks_asyncio(2)]
    loop.run_until_complete(asyncio.wait(tasks)) # 执行任务
    loop.close()
if __name__ == '__main__':
    distribute_lagou()