# 子项目的常量定义
"""
    拉勾相关网页
"""
FINANCE_STAGE_DICT = {
    '未融资': 1,
    '天使轮': 2,
    'A轮': 3,
    'B轮': 4,
    'C轮': 5,
    'D轮及以上': 6,
    '上市公司': 7,
    '不需要融资': 8,
}

INDUSTRY_FIELD = {
    "移动互联网":24,
    '电子商务':25,
    '金融':33,
    '企业服务':27,
    '教育':29,
    '文化娱乐':45,
    '游戏':31,
    'O2O':28,
    '硬件':47,
    '医疗健康':34,
    '生活服务':35,
    '广告营销':43,
    '旅游':32,
    '数据服务':41,
    '社交网络':26,
    '分类信息':48,
    '信息安全':38,
    '招聘':49,
    '其他':10594
}

"""
    工作性质
"""
JOB_NATURE_DICT = {
    '全职': 0,
    '兼职': 1,
    '实习': 2,
}

COMPANY_SIZE_DICT = {
    'unknown': 0,
    '15-50人': 1,
    '50-150人': 2,
    '150-500人': 3,
    '500-2000人': 4,
    '2000人以上': 5,
    '少于15人': 6,
}

HTTP_HEADER = {
    'Host': 'www.lagou.com',
    'Referer': 'https://www.lagou.com/gongsi/',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'X-Anit-Forge-Code': '0',
    'DNT': '1',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.6,en;q=0.4,en-US;q=0.2,en-GB;q=0.2',
    'Connection': 'keep-alive',
    'Cache-Control': 'no-cache',
    'Origin': 'https//www.lagou.com',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'X-Requested-With': 'XMLHttpRequest',
    'X-Anit-Forge-Token': 'None',
    'Pragma': 'no-cache',
    'Upgrade-Insecure-Requests': '1',
}

WORK_YEARS_REQUEST_DICT = {
    'unknown': 0,
    '1-3年': 1,
    '10年以上': 2,
    '3-5年': 3,
    '5-10年': 4,
    '不限': 5,
    '应届毕业生': 6,
    '1年以下': 7,
}

PROJECT = '拉勾'

# 获取详细职位id信息的json请求地址
JOB_JSON_URL = 'https://www.lagou.com/jobs/positionAjax.json'

# 获取职位详情的页面
JOB_DETAIL_URL = 'https://www.lagou.com/jobs/{job_id}.html'

# 获取公司详情页面的地址
COMPANY_DETAIL_URL = 'https://www.lagou.com/gongsi/{company_id}.html'

# 所有城市地址
ALL_CITY_URL = 'https://www.lagou.com/gongsi/allCity.html?option=0-0-0'

# 获取所有公司地址. 0-0-0.json
CITY_COMPANY_URL = 'https://www.lagou.com/gongsi/{0}-{1}-{2}.json'

# 公司-职位对应地址
COMPANY_JOB_URL = 'https://www.lagou.com/gongsi/searchPosition.json'

DIS_QUEUE = 'steve:lagou'