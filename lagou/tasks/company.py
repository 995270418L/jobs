# 爬取所有公司的信息

import logging
import requests
from requests.exceptions import RequestException
from common import constants
from math import ceil
from lagou.utils.http_tools import generate_http_header, filter_http_tag
from lagou.utils.cookies import Cookies
from common.util import crawl_sleep
from common.exceptions import RequestsError
from lagou.domain.CompanyModel import CompanyModel
from lagou.common_s import constants as constants_s
from lxml import etree

logger = logging.getLogger(__name__)

# 按照城市来更新公司数据
def update_company_data(city_id, finance_stage_id, industry_id):
    logger.info("正在爬取{0}的，所在行业为{1},融资类型为{1}的公司数据".format(city_id,finance_stage_id,industry_id))
    url = constants_s.CITY_COMPANY_URL.format(city_id,finance_stage_id,industry_id)
    response = request_company_json(url, page_no=1)
    # 计算需要爬取的页数
    page_count = int(ceil(int(response['totalCount']) / int(response['pageSize'])))
    for page_no in range(1, page_count + 1):
        logger.info('正在爬取城市={}, 融资类型={}, 行业类别={}, 第 「{}」 页'.format(city_id, finance_stage_id, industry_id, page_no))
        response = request_company_json(url=url, page_no=page_no)
        companys = response['result']
        logging.info("总公司数: {}".format(len(companys)))
        if len(companys) == 0:
            logging.info('json数据返回为空，所在位置: company.py -> update_company_data')
            break
        for company in companys:
            company_id = int(company['companyId'])
            if CompanyModel.count(id=company_id) == 0:
                generate_company_data(company=company, city_id=city_id)
            # 更新公司下职位的数据
            # if not redis_instance.sismember(constants.REDIS_VISITED_COMPANY_KEY, company_id):
            #     redis_instance.sadd(constants.REDIS_VISITED_COMPANY_KEY, company_id)
            #     update_job_data(company_id=company_id)
    logger.info('爬取城市={}, 融资类型={}, 行业类别={}, 任务结束'.format(city_id, finance_stage_id, industry_id))

def request_company_json(url, page_no):
    prams = {
        'first': False,
        'pn': page_no,
        'sortField': 1,
        'havemark': 0,
    }
    headers = generate_http_header()
    crawl_sleep()
    try:
        cookies = Cookies.get_random_cookies()
        response_json = requests.get(
            url=url,
            params=prams,
            headers=headers,
            cookies=cookies,
            allow_redirects=False,
            timeout=constants.TIMEOUT).json()
        if 'totalCount' not in response_json:
            Cookies.remove_cookies(cookies)
            raise RequestsError(error_log='wrong response content')
    except RequestException as e:
        logging.error(e)
        raise RequestsError(error_log=e)
    return response_json

def generate_company_data(company, city_id):
    """生成公司数据"""
    com_id = company['companyId']
    com_name = filter_http_tag(company['companyShortName'])
    com_fullname = filter_http_tag(company['companyFullName'])
    com_process = filter_http_tag(company['financeStage']).upper()
    if com_process not in constants_s.FINANCE_STAGE_DICT:
        logger.error(company['financeStage'] + 'not in FINANCE_STAGE_DICT')
    finance_stage = constants_s.FINANCE_STAGE_DICT[com_process] \
        if com_process in constants_s.FINANCE_STAGE_DICT else constants_s.FINANCE_STAGE_DICT['unknown']
    com_resume_rate = company['processRate'] if 'processRate' in company else -1
    features = filter_http_tag(company['companyFeatures'])
    advantage, address, size, introduce = requests_company_detail_data(company_id=com_id)
    company = {
        'id':com_id,
        'com_name':com_name,
        'com_fullname':com_fullname,
        'com_process':com_process,
        'finance_stage':finance_stage,
        'com_resume_rate':com_resume_rate,
        'features':features,
        'advantage':advantage,
        'address':address,
        'size':size,
        'introduce':introduce
    }
    print(company)
    # CompanyController.add(
    #     id=company_id,
    #     shortname=shortname,
    #     fullname=fullname,
    #     finance_stage=finance_stage,
    #     process_rate=process_rate,
    #     city_id=city_id,
    #     features=features,
    #     advantage=advantage,
    #     address=address,
    #     size=size,
    #     introduce=introduce,
    # )
    # industry_fields = set(re.split(",|，|、", company['industryField']))
    # for industry_field in industry_fields:
    #     industry_id = IndustryController.get_industry_id_by_name(industry_field)
    #     CompanyIndustryController.add(company_id, industry_id, city_id)

def requests_company_detail_data(company_id):
    """请求公司详情页数据"""
    headers = generate_http_header()
    crawl_sleep()
    try:
        response = requests.get(
            url=constants_s.COMPANY_DETAIL_URL.format(company_id=company_id),
            headers=headers,
            cookies=Cookies.get_random_cookies(),
            allow_redirects=False,
            timeout=constants.TIMEOUT)
    except RequestException as e:
        logging.error(e)
        raise RequestsError(error_log=e)
    html = etree.HTML(response.text)
    advantage = html.xpath('//div[@id="tags_container"]//li/text()')
    size = html.xpath('//div[@id="basic_container"]//li[3]/span/text()')
    address = html.xpath('//p[@class="mlist_li_desc"]/text()')
    introduce = html.xpath('//span[@class="company_content"]//text()')

    return format_tag(advantage, address, size, introduce, company_id)


def format_tag(advantage, address, size, introduce, company_id=None):
    """格式化数据"""
    if len(advantage) == 0:
        logger.warning('advantage is None, company id is {}'.format(company_id))
        advantage = ''
    else:
        advantage = ','.join(map(filter_http_tag, advantage))

    if len(introduce) == 0:
        logger.warning('introduce is None, company id is {}'.format(company_id))
        introduce = ''
    else:
        introduce = '  '.join(map(filter_http_tag, introduce))

    if len(address) == 0:
        logger.warning('address is None, company id is {}'.format(company_id))
        address = ''
    else:
        address = filter_http_tag(address[0])

    if len(size) == 0 or size[0] not in constants_s.COMPANY_SIZE_DICT:
        logger.error('size is None or error format, company id is {}'.format(company_id))
        size = 'unknown'
    else:
        size = filter_http_tag(size[0])

    return advantage, address, constants_s.COMPANY_SIZE_DICT[size], introduce

