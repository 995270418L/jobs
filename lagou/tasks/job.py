# 爬取工作信息详情
import logging
import uuid
from json import JSONDecodeError
from math import ceil
import requests
from bs4 import BeautifulSoup
from common import constants
from common.exceptions import RequestsError
from common.util import crawl_sleep
from lagou.common_s import constants as constants_s
from lagou.domain.CityModel import CityModel
from lagou.domain.JobModel import JobModel
from lagou.domain.JobTagModel import JobTagModel
from lagou.domain.JobTagRModel import JobTagRModel
from lagou.utils.cookies import Cookies
from lagou.utils.http_tools import generate_http_header, filter_http_tag

logger = logging.getLogger(__name__)
# 根据公司id获取所有工作
def update_job_data(company_id,isSchool):
    """更新职位数据"""
    logger.info("正在获取公司id为:{0}的{1}工作信息".format(company_id, "学校招聘" if isSchool else "社会招聘"))
    response = request_job_json(company_id=company_id, page_no=1)
    # 计算该公司职位的页数
    page_count = int(ceil(
        int(response['content']['data']['page']['totalCount']) / int(response['content']['data']['page']['pageSize'])))
    for page_no in range(1, page_count + 1):
        json_result = request_job_json(company_id=company_id, page_no=page_no)
        jobs = json_result['content']['data']['page']['result']
        for job in jobs:
            job_id = job['positionId']
            # if JobModel.count(job_id=int(job_id)) == 0:
            generate_job_data(job, company_id)

def generate_job_data(job, company_id):
    """生成职位数据"""
    id = str(uuid.uuid1())
    job_attract, job_descr, tags,job_site = requests_job_detail_data(job['positionId'])
    job_id = job['positionId']
    job_place_id = 0 if 'city' not in job else CityModel.get_city_id_by_name(job['city']).city_id
    job_name = job['positionName']
    job_exper = filter_http_tag(job['workYear'])
    job_salary = job['salary']
    job_record = job['education']
    job_create_time = job['createTime']
    job_m = JobModel(id=id,job_id=str(job_id),job_name=job_name,job_salary=job_salary,job_place_id=job_place_id,job_exper=job_exper,job_record=job_record,
                     job_attract=job_attract,job_descr=job_descr,job_site=job_site,job_create_time=job_create_time,com_id=company_id)
    JobModel.add(job_m)
    job_tag_rs = []
    for tag in tags:
        tag_id = JobTagModel.find_by_name(tag)
        job_tag_r = JobTagRModel(id=str(uuid.uuid1()),job_id=job_id,tag_id=tag_id)
        job_tag_rs.append(job_tag_r)
    JobTagRModel.add_all(job_tag_rs)

def requests_job_detail_data(job_id):
    """请求职位详情页数据"""
    url = constants_s.JOB_DETAIL_URL.format(job_id=job_id)
    logger.info('正在请求工作详情页，url为: {}'.format(url))
    headers = generate_http_header()
    crawl_sleep()
    try:
        response = requests.get(
            url=url,
            headers=headers,
            cookies=Cookies.get_random_cookies(),
            allow_redirects=False,
            timeout=constants.TIMEOUT)
        if response.status_code == 302:
            Cookies.refresh_cookies()
            return requests_job_detail_data(job_id)
    except Exception as e:
        logger.error('请求url:{0} 失败，响应码: {1},异常信息:{2},检查对应服务器是否能正常上网.'.format(url,response.status_code,e))
        raise RequestsError
    html = BeautifulSoup(response.text,'lxml')
    try:
        job_attract = ''.join(html.select('.job-advantage p')[0].stripped_strings)
    except IndexError:
        job_attract = '无职位诱惑'
    try:
        job_descr = ''.join(html.select('.job_bt div')[0].stripped_strings)
    except IndexError:
        job_descr = '无职位描述'
    job_tags = html.select('.position-label li')
    tags = []
    for job_tag in job_tags:
        tag = ''.join(job_tag.stripped_strings)
        tags.append(tag)
    return job_attract,job_descr,tags,url

def request_job_json(company_id, page_no,isSchool=False):
    prams = {
        'companyId': company_id,
        'positionFirstType': "全部",
        'pageNo': page_no,
        'schoolJob': 'true' if isSchool else 'false',
        'pageSize': 10,
    }
    headers = generate_http_header()
    crawl_sleep()
    try:
        cookies = Cookies.get_random_cookies()
        response_data= requests.post(
            url=constants_s.COMPANY_JOB_URL,
            data=prams,
            headers=headers,
            cookies=cookies,
            timeout=constants.TIMEOUT)
        response_json = response_data.json()
        if 'content' not in response_json:
            Cookies.remove_cookies(cookies)
            logger.warning('cookies失效，正在重新获取')
            return request_job_json(company_id,page_no,isSchool)
    except JSONDecodeError as e:
        logger.warning("json数据解析失败，请检查地址是否失效，错误信息:{}".format(e))
        return request_job_json(company_id,page_no,isSchool)
    except Exception as e :
        logger.error('请求url:{0} 失败，响应码: {1},异常信息:{2},检查对应服务器是否能正常上网.'.format(constants_s.COMPANY_JOB_URL,response_data.status_code,e))
        raise RequestsError
    return response_json