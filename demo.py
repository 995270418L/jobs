import requests
import time
import threading

url = 'https://www.lagou.com/gongsi/allCity.html?option=0-0-0'
# 测试接口的响应速度
def request():
    start = time.time()
    requests.get("http://10.0.0.2:1024/company/one?name=steve&age=10&sex=true").text
    print("响应时间: {} ms".format((time.time() - start)))

for i in range(1,1000):
    request()