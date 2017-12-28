# coding=utf-8
import time
import random
import logging
import requests

from common import constants,proxy

class Cookies(object):
    _cookies = []
    _last_update_time = None

    @classmethod
    def refresh_cookies(cls):
        """刷新 cookie """
        proxys = proxy.get_proxy()
        cls._cookies = cls.get_lagou_cookies_from_proxys(proxys)
        cls._last_update_time = time.time()

    @classmethod
    def get_random_cookies(cls):
        now = time.time()
        # cookie 超时时间
        if len(cls._cookies) == 0 or (now - cls._last_update_time) >= constants.SECONDS_OF_DAY :
            cls.refresh_cookies()
        return random.choice(cls._cookies)

    @classmethod
    def remove_cookies(cls, cookies):
        cls._cookies.remove(cookies)

    @classmethod
    def get_lagou_cookies_from_proxys(cls, proxy_m, proxy_type='http'):
        logging.info('重新获取 cookies !')
        logging.info('代理 IP 的地址:{}'.format(proxy_m))
        cookies = []
        retry_count = constants.RETRY_COUNT
        while retry_count > 0:
            try:
                response = requests.get('https://www.lagou.com/',
                                        proxies={proxy_type: proxy_m},
                                        allow_redirects=False,
                                        timeout=2)
                if len(response.cookies):
                    cookies.append(response.cookies)
                logging.info('可用 cookies 数量: {}'.format(len(cookies)))
                return cookies
            except Exception:
                retry_count -= 1
        logging.debug("当前代理ip: {} 不能用,请重新获取一个再试".format(proxy_m))
        proxy.delete_proxy(proxy_m)
        return None