# 爬取所有公司的信息

import logging
import re
import uuid
from json import JSONDecodeError
from math import ceil
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import asyncio
from common import constants
from common.exceptions import RequestsError
from common.util import crawl_sleep
from lagou.common_s import constants as constants_s
from lagou.domain.CompanyModel import CompanyModel
from lagou.domain.ComTagRModel import ComTagRModel
from lagou.domain.ComFieldRModel import ComFieldRModel
from lagou.domain.ComTagModel import ComTagModel
from lagou.domain.ComFieldModel import ComFieldModel
from lagou.utils.cookies import Cookies
from lagou.utils.http_tools import generate_http_header, filter_http_tag
from lagou.tasks import job

logger = logging.getLogger(__name__)

def distribute(url):
    result = re.findall(r'\d+',url)
    if len(result) == 3:
        city_id = result[0]
        finance_stage_id = result[1]
        industry_id = result[2]
        update_company_data(city_id=city_id,finance_stage_id=finance_stage_id,industry_id=industry_id)
    else:
        logger.warning('url格式错误:{}'.format(url))

# 按照城市来更新公司数据
def update_company_data(city_id, finance_stage_id, industry_id):
    # 先清空表
    #CompanyModel.delete_all()
    url = constants_s.CITY_COMPANY_URL.format(city_id,finance_stage_id,industry_id)
    response = request_company_json(url, page_no=1)
    # 计算需要爬取的页数
    page_count = int(ceil(int(response['totalCount']) / int(response['pageSize'])))
    if page_count == 0:
        logger.error("地址为: " + url + " 的页面获取不到数据了，请注意检查代码配置")
        return
    for page_no in range(1, page_count + 1):
        logger.info('正在爬取城市={}, 融资类型={}, 行业类别={}, 第 「{}」 页'.format(city_id, finance_stage_id, industry_id, page_no))
        response = request_company_json(url=url, page_no=page_no)
        companys = response['result']
        if len(companys) == 0:
            logger.info('json数据返回为空，所在位置: company.py -> update_company_data')
            continue
        # asyncio_crawler(companys)
        for company in companys:
            company_id = int(company['companyId'])
            # if CompanyModel.count(id=company_id) == 0:
            generate_company_data(company=company,city_id=city_id)
    logger.info('爬取城市={}, 融资类型={}, 行业类别={}, 任务结束'.format(city_id, finance_stage_id, industry_id))
# def asyncio_crawler(companys):
#     loop = asyncio.get_event_loop()
#     tasks = [generate_company_data(company=company, city_id=company['companyId']) for company in companys]
#     loop.run_until_complete(asyncio.wait(tasks))
#     loop.close()

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
        response_json = requests.post(
            url=url,
            params=prams,
            headers=headers,
            cookies=cookies,
            allow_redirects=False,
            timeout=constants.TIMEOUT).json()
        if 'totalCount' not in response_json:
            Cookies.remove_cookies(cookies)
            return request_company_json(url,page_no)
    except JSONDecodeError as e:
        logger.error(e)
        return request_company_json(url,page_no)
    except ConnectionError as e :
        logger.error("建立连接失败，url:{0},请检查网络情况,异常信息: {1}".format(url,e))
    return response_json

def generate_company_data(company, city_id):
    """生成公司数据"""
    id = str(uuid.uuid1())
    com_id = company['companyId']
    com_name = filter_http_tag(company['companyShortName'])
    com_fullname = filter_http_tag(company['companyFullName'])
    com_process = filter_http_tag(company['financeStage']).upper()
    if com_process not in constants_s.FINANCE_STAGE_DICT:
        logger.error(company['financeStage'] + 'not in FINANCE_STAGE_DICT')
    finance_stage = constants_s.FINANCE_STAGE_DICT[com_process] \
        if com_process in constants_s.FINANCE_STAGE_DICT else constants_s.FINANCE_STAGE_DICT['unknown']
    com_resume_rate = company['processRate'] if 'processRate' in company else -1
    com_record_time = datetime.today()
    tags, com_number, address, introduce,com_social_num,com_school_num,com_site = requests_company_detail_data(company_id=com_id)
    company_m =CompanyModel(id=id,com_id=str(com_id),com_name=com_name,com_process=finance_stage,com_number=com_number,com_city_id=city_id,
                          com_num_school=com_school_num,com_num_social=com_social_num,com_site=com_site,com_source='拉勾',com_fullname=com_fullname,
                          com_address=address,com_info=introduce,com_record_time=com_record_time,com_resume_rate=com_resume_rate)
    # 公司表插入 异步IO实现
    CompanyModel.add(company_m)
    # 公司标签R 表插入
    com_tag_rs = []
    for tag in tags:
        tag_id = ComTagModel.find_by_name(tag)
        com_id_f = id
        id= str(uuid.uuid1())
        com_tag_r = ComTagRModel(id=id,com_id=com_id_f,tag_id=tag_id)
        com_tag_rs.append(com_tag_r)
    ComTagRModel.add_all(com_tag_rs)
    com_field_rs = []
    industry_fields = set(re.split(",|，|、", company['industryField']))
    for industry_field in industry_fields:
        # 行业id
        industry_id = ComFieldModel.find_by_name(industry_field)
        # 表主键id
        field_id = str(uuid.uuid1())
        com_field_r = ComFieldRModel(id=field_id,com_id=id,field_id=industry_id)
        com_field_rs.append(com_field_r)
    # 公司行业R 插入
    ComFieldRModel.add_all(com_field_rs)
    # 开始生成job数据
    if int(com_social_num) != 0 and com_school_num != 0:
        job.update_job_data(com_id,True)
        job.update_job_data(com_id,False)
    if int(com_social_num) != 0 and com_school_num == 0:
        job.update_job_data(com_id,False)
    if int(com_social_num) == 0 and com_school_num != 0:
        job.update_job_data(com_id,True)


def requests_company_detail_data(company_id):
    """请求公司详情页数据"""
    url = constants_s.COMPANY_DETAIL_URL.format(company_id=company_id)
    logger.info("正在请求公司详情页数据,url: {}".format(url))
    headers = generate_http_header()
    crawl_sleep()
    try:
        cookies = Cookies.get_random_cookies()
        response = requests.get(
            url= url,
            headers=headers,
            cookies=cookies,
            allow_redirects=False,
            timeout=constants.TIMEOUT)
        if int(response.status_code) == 302:
            logger.info('cookies 信息失效，重新获取')
            Cookies.remove_cookies(cookies)
            return requests_company_detail_data(company_id)
    except Exception as e:
        logger.error('请求url:{0} 失败，响应码: {1},异常信息:{2},检查对应服务器是否能正常上网.'.format(url,response.status_code,e))
        raise RequestsError
    html = BeautifulSoup(response.text,'lxml')
    com_tags = html.select('#tags_container li')
    tags = []
    for com_tag in com_tags:
        tag = ''.join(com_tag.stripped_strings)
        tags.append(tag)
    # 公司的规模(人数)
    try:
        com_number = ''.join(html.select('.number')[0].next_sibling.next_sibling.stripped_strings)
    except IndexError:
        com_number = '0'
    try:
        address = "".join(html.select('.mlist_li_desc')[0].stripped_strings)
    except IndexError:
        address = '无地址'
    # 公司简介
    try:
        introduce = ''.join(html.select('.company_content')[0].stripped_strings)
    except IndexError:
        introduce = ''
    # 社招职位
    li_tag = html.find_all('li',class_="current")[0]
    social_tag = li_tag.next_sibling.next_sibling
    social_jobs = ''.join(social_tag.stripped_strings)
    try:
        com_social_num = re.findall(r'\d+',social_jobs)[0]
    except IndexError:
        com_social_num = 0
    # 校招职位
    school_tag =''.join(social_tag.next_sibling.next_sibling.stripped_strings)
    com_school_num = re.findall(r'\d+', school_tag)
    if len(com_school_num) > 0 :
        com_school_num = com_school_num[0]
    else:
        com_school_num = 0
    try:
        com_site = html.select('.hovertips')[0]['href']
    except KeyError:
        com_site = url
    if len(com_site) > 493 :
        com_site = com_site[0:497]+'...'
    return tags,com_number,address,introduce,com_social_num,com_school_num,com_site