import requests
import random
from common import constants
from common.db import redis_instance

# 获取多个代理ip
def get_proxy():
    key = redis_instance.hgetall(name=constants.REDIS_NAME)
    rkey = random.choice(list(key.keys())) if key else None
    if isinstance(rkey, bytes):
        return rkey.decode('utf-8')
    else:
        return rkey

def delete_proxy(proxy):
    redis_instance.hdel(constants.REDIS_NAME,proxy)

# your spider code
def getHtml(url):
    retry_count = constants.RETRY_COUNT
    proxy = get_proxy()
    while retry_count > 0:
        try:
            html = requests.get(url, proxies={"http": "http://{}".format(proxy)})
            # 使用代理访问
            return html
        except Exception:
            retry_count -= 1
    # 出错5次, 删除代理池中代理
    delete_proxy(proxy)
    return None

# def main():
#     # redis_instance.hset('steve','lxh','123')
#     key = redis_instance.hgetall('useful_proxy')
#     print(key)
# if __name__ == '__main__':
#     main()