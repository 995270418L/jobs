import requests
from common import constants

# 获取多个代理ip
def get_proxy():
    return requests.get("http://127.0.0.1:5051/get/").content

def delete_proxy(proxy):
    requests.get("http://127.0.0.1:5051/delete/?proxy={}".format(proxy))

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