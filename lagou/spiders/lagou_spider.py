# -*- coding: utf-8 -*-
import scrapy
import logging
from scrapy import Request
from lagou.items import LagouItem
import json
import codecs
import uuid
from lagou.utils.util import *
from lagou.utils.login import *
from scrapy.conf import settings

logger = logging.getLogger('jintao')


def get_uuid():
    return str(uuid.uuid4())


class LagouSpider(scrapy.Spider):
    name = 'lagou'
    allowed_domains = ['lagou.com']

    kd = '会计'

    cookie = "JSESSIONID=" + get_uuid() + ";" \
                                          "user_trace_token=" + get_uuid() + "; LGUID=" + get_uuid() + "; index_location_city=%E6%88%90%E9%83%BD; " \
                                                                                                       "SEARCH_ID=" + get_uuid() + '; _gid=GA1.2.717841549.1514043316; ' \
                                                                                                                                   '_ga=GA1.2.952298646.1514043316; ' \
                                                                                                                                   'LGSID=' + get_uuid() + "; " \
                                                                                                                                                           "LGRID=" + get_uuid() + "; "

    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        # 'Cookie': '_ga=GA1.2.1675705296.1525503483; user_trace_token=20180505145804-a854ed80-5031-11e8-869c-525400f775ce; LGUID=20180505145804-a854f0b2-5031-11e8-869c-525400f775ce; _gid=GA1.2.1639933130.1525856914; index_location_city=%E6%B7%B1%E5%9C%B3; JSESSIONID=ABAAABAACEBACDG04FABB7BD87B79FAC311DCA849B647AD; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1525503484,1525869827; X_HTTP_TOKEN=a182ed869a8003910c5f297e88d8d0ce; X_MIDDLE_TOKEN=08efdfbc4e46f32d79b4965ed35ed919; LGSID=20180510142346-b222b4ee-541a-11e8-81e3-5254005c3644; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1525938024; LGRID=20180510154024-663ed077-5425-11e8-93e9-525400f775ce; TG-TRACK-CODE=search_code; SEARCH_ID=be579ebfc13249c4b2dfbcef8a093f71',
        'Cookie': cookie,
        'Host': 'www.lagou.com',
        'Origin': 'https://www.lagou.com',
        'Referer': 'https://www.lagou.com/jobs/list_%E4%BC%9A%E8%AE%A1?labelWords=&fromSearch=true&suginput=',
        'User-Agent': 'User-Agent:Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
        'X-Anit-Forge-Code': '0',
        'X-Anit-Forge-Token': 'None',
        'X-Requested-With': 'XMLHttpRequest'}


    def __init__(self, *args, **kwargs):
        # 拉勾登录账号密码
        self._username = ''#settings['USERNAME']
        self._password = ''#settings['PASSWORD']

        # login_cookies
        self.login_cookies = None

        # 爬取字段 set到referer_name中
        self.kd = '会计'
        settings.set("REFERER_NAME", self.kd)

        # 页数设个起始值
        self.page_no = 1

        # 请求json的url
        self._url = 'https://www.lagou.com/jobs/positionAjax.json?px=new&kd={}&pn={}&'

        super(LagouSpider, self).__init__(*args)


    # def start_requests(self):
    #     # 登录
    #     login(user=self._username, pass_wd=self._password)
    #     self.login_cookies = self.cookie
    #     # logger.info(self.login_cookies)
    #
    #     url = self._url.format(self.kd, self.page_no)
    #
    #     yield scrapy.Request(
    #         url=url,
    #         method="GET",
    #         callback=self.parse,
    #         headers=self.headers
    #     )

    def start_requests(self):
        url = 'https://www.lagou.com/jobs/positionAjax.json?city=%E6%B7%B1%E5%9C%B3&needAddtionalResult=false'
        yield scrapy.FormRequest(url, formdata={'first': 'true', 'pn': '1', 'kd': self.kd}, method='Post',
                                 meta={'pn': 1}, headers=self.headers, callback=self.parse)

    def parse(self, response):
        # print(response.url)
        html = response.text
        data = json.loads(html)
        if data:
            content = data.get('content')
            positionResult = content.get('positionResult')
            totalCount = positionResult.get('totalCount')

            pages = int(totalCount / 15)

            if pages >= 50:
                pages = 50
            else:
                pages = pages

            results = positionResult.get('result')
            for result in results:
                item = LagouItem()
                item['companyFullName'] = result.get('companyFullName')
                item['companyId'] = result.get('companyId')
                item['companyLabelList'] = result.get('companyLabelList')
                item['companyLogo'] = result.get('companyLogo')
                item['companyShortName'] = result.get('companyShortName')
                item['companySize'] = result.get('companySize')
                item['createTime'] = result.get('createTime')
                item['deliver'] = result.get('deliver')
                item['district'] = result.get('district')
                item['education'] = result.get('education')
                item['explain'] = result.get('explain')
                item['financeStage'] = result.get('financeStage')
                item['firstType'] = result.get('firstType')
                item['formatCreateTime'] = result.get('formatCreateTime')
                item['gradeDescription'] = result.get('gradeDescription')
                item['industryField'] = result.get('industryField')
                item['industryLables'] = result.get('industryLables')
                item['isSchoolJob'] = result.get('isSchoolJob')
                item['jobNature'] = result.get('jobNature')
                item['positionAdvantage'] = result.get('positionAdvantage')
                item['positionId'] = result.get('positionId')
                item['positionLables'] = result.get('positionLables')
                item['positionName'] = result.get('positionName')
                item['salary'] = result.get('salary')
                item['secondType'] = result.get('secondType')
                item['workYear'] = result.get('workYear')
                # 公司页面url
                company_url = 'https://www.lagou.com/gongsi/%s.html' % item['companyId']
                # 招聘信息页面url
                job_url = 'https://www.lagou.com/jobs/%s.html' % item['positionId']
                item['work_info_url'] = job_url
                item['companyUrl'] = company_url
                yield item
                # yield scrapy.Request(
                #     url=job_url,
                #     method="GET",
                #     cookies=self.cookie,
                #     callback=self.parse_job_info,
                #     headers=self.headers,
                #     meta={
                #         "item": item,
                #         "company_url": company_url
                #     },
                #     dont_filter=False
                # )

            pn = int(response.meta.get('pn')) + 1
            if pn <= pages:
                yield scrapy.FormRequest(response.url, formdata={'first': 'False', 'pn': str(pn), 'kd': self.kd},
                                         method='Post', meta={'pn': pn}, headers=self.headers, callback=self.parse)

    # def parse_job_info(self, response):
    #     """
    #     解析职位信息
    #     :param response:
    #     :return:
    #     """
    #     # Item
    #     item = response.meta['item']
    #
    #     # 企业URL
    #     company_url = response.meta['company_url']
    #
    #     info = response.xpath("//dd[@class='job_bt']//p/text()").extract()
    #
    #     if len(info) != 0:
    #         # item['work_content'] = get_value(info)
    #         item['work_content'] = info
    #     else:
    #         info = response.xpath("//dd[@class='job_bt']//p/span/text()").extract()
    #         # item['work_content'] = get_value(info)
    #         item['work_content'] = info
    #
    #     yield item
    #     # yield scrapy.Request(url=company_url,
    #     #                      method="GET",
    #     #                      cookies=self.cookie,
    #     #                      callback=self.parse_company_info,
    #     #                      meta={
    #     #                          "item": item
    #     #                      },
    #     #                      dont_filter=True)

    # @staticmethod
    # def parse_company_info(response):
    #     """
    #     解析企业信息
    #     :param response:
    #     :return:
    #     """
    #
    #     # Item
    #     item = response.meta['item']
    #     print response.xpath(
    #         'string(//*[@id="companyInfoData"])'
    #     ).extract()[0]
    #     # 获取页面上的json, 并解析
    #     business_json = json.loads(response.xpath(
    #         'string(//*[@id="companyInfoData"])'
    #     ).extract()[0])
    #
    #     # 公司地址（判断）
    #     try:
    #         address_list = business_json['addressList'][0]
    #         business_location = address_list['province'] + address_list['city'] + address_list['district']
    #     except KeyError:
    #         try:
    #             address_list = business_json['addressList'][1]
    #             business_location = address_list['province'] + address_list['city'] + address_list['district']
    #
    #         except (IndexError, KeyError):
    #             business_location = ""
    #
    #     # 公司地址
    #     item['companyLocation'] = business_location
    #
    #     # 公司网站主页
    #     item['companyWebsite'] = business_json['coreInfo']['companyUrl']
    #
    #     # 公司介绍
    #     try:
    #         business_info = business_json['introduction']['companyProfile']
    #         business_info = filter_html_tag(content=business_info). \
    #             replace("\n", ""). \
    #             replace("&nbsp;", "")
    #
    #     except KeyError:
    #         business_info = ""
    #
    #     # 公司介绍信息
    #     item['companyInfo'] = business_info
    #
    #     yield item
