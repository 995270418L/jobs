# coding=utf-8
import time
import random
import logging
import requests

from common import constants,proxy

logger = logging.getLogger(__name__)
class Cookies(object):
    _cookies = None
    _last_update_time = None

    @classmethod
    def refresh_cookies(cls):
        """刷新 cookie """
        proxys = proxy.get_proxy()
        cookies = cls.get_lagou_cookies_from_proxys(proxys)
        if cookies is None:
            logger.error("代理失效，正在重新获取")
            return cls.refresh_cookies()
        cls._cookies = cookies
        cls._last_update_time = time.time()

    @classmethod
    def get_random_cookies(cls):
        now = time.time()
        # cookie 超时时间
        if cls._cookies is None or (now - cls._last_update_time) >= constants.SECONDS_OF_DAY :
            cls.refresh_cookies()
        return cls._cookies

    @classmethod
    def remove_cookies(cls, cookies):
        cls._cookies = None

    @classmethod
    def get_lagou_cookies_from_proxys(cls, proxy_m, proxy_type='http'):
        logger.info('代理 IP 的地址:{}'.format(proxy_m))
        retry_count = constants.RETRY_COUNT
        while retry_count > 0:
            try:
                response = requests.get('https://www.lagou.com/',
                                        proxies={proxy_type: proxy_m},
                                        allow_redirects=False,
                                        timeout=2)
                if response.cookies is None:
                    return cls.get_lagou_cookies_from_proxys(proxy_m)
                return response.cookies
            except Exception:
                retry_count -= 1
        logger.warning("当前代理ip: {} 不能用,已被删除".format(proxy_m))
        proxy.delete_proxy(proxy_m)
        return None