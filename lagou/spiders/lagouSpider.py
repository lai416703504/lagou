# -*- coding: utf-8 -*-

# 内置库
import json
import random

# 第三方库
import scrapy

# 项目内部的库
from lagou.items import LagouItem
from lagou.user_agents import agents


# 日志中心
# logger = Logger(logger='lagouSpider.py').get_logger()


class LagouSpider(scrapy.Spider):
    name = "lagou"

    start_urls = [
        'https://www.lagou.com/zhaopin/'
    ]

    custom_settings = {
        "COOKIES_ENABLED": False,
        "DOWNLOAD_DELAY": 1,
        'DEFAULT_REQUEST_HEADERS': {
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Connection": "keep-alive",
            "Content-Length": "37",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Cookie": "_ga=GA1.2.115650928.1527149777; user_trace_token=20180524161623-bf4cc840-5f2a-11e8-9641-525400f775ce; LGUID=20180524161623-bf4ccc82-5f2a-11e8-9641-525400f775ce; JSESSIONID=ABAAABAAAFCAAEG5B94983D56B37B034A9C3A8E91CB59A4; _gid=GA1.2.8157721.1527727634; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1527149777,1527727634; index_location_city=%E6%B7%B1%E5%9C%B3; TG-TRACK-CODE=index_search; X_HTTP_TOKEN=a2ffb8c4d6bd7746e3c043272d233108; showExpriedIndex=1; showExpriedCompanyHome=1; showExpriedMyPublish=1; hasDeliver=57; login=false; unick=""; _putrc=""; LG_LOGIN_USER_ID=""; LGRID=20180531145912-1f891dfd-64a0-11e8-8ba3-525400f775ce; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1527749946; SEARCH_ID=0192edbec51a422697ac623eda64a102",
            "Host": "www.lagou.com",
            "Origin": "https://www.lagou.com",
            "Referer": "https://www.lagou.com/jobs/list_%E4%BC%9A%E8%AE%A1?labelWords=&fromSearch=true&suginput=",
            "User-Agent": random.choice(agents),
            "X-Anit-Forge-Code": "0",
            "X-Anit-Forge-Token": "None",
            "X-Requested-With": "XMLHttpRequest"
        }
    }

    totalPageCount = 0
    curpage = 1
    cur = 0
    myurl = 'https://www.lagou.com/jobs/positionAjax.json?px=new&city=%E6%B7%B1%E5%9C%B3&needAddtionalResult=false'

    city = u'深圳'
    kds = [u'会计', u'审计']
    kd = kds[0]
    HEADER = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Connection": "keep-alive",
        "Content-Length": "37",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Cookie": "_ga=GA1.2.115650928.1527149777; user_trace_token=20180524161623-bf4cc840-5f2a-11e8-9641-525400f775ce; LGUID=20180524161623-bf4ccc82-5f2a-11e8-9641-525400f775ce; JSESSIONID=ABAAABAAAFCAAEG5B94983D56B37B034A9C3A8E91CB59A4; _gid=GA1.2.8157721.1527727634; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1527149777,1527727634; index_location_city=%E6%B7%B1%E5%9C%B3; TG-TRACK-CODE=index_search; X_HTTP_TOKEN=a2ffb8c4d6bd7746e3c043272d233108; showExpriedIndex=1; showExpriedCompanyHome=1; showExpriedMyPublish=1; hasDeliver=57; login=false; unick=""; _putrc=""; LG_LOGIN_USER_ID=""; LGRID=20180531145912-1f891dfd-64a0-11e8-8ba3-525400f775ce; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1527749946; SEARCH_ID=0192edbec51a422697ac623eda64a102",
        "Host": "www.lagou.com",
        "Origin": "https://www.lagou.com",
        "Referer": "https://www.lagou.com/jobs/list_%E4%BC%9A%E8%AE%A1?labelWords=&fromSearch=true&suginput=",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36",
        "X-Anit-Forge-Code": "0",
        "X-Anit-Forge-Token": "None",
        "X-Requested-With": "XMLHttpRequest"
    }

    def start_requests(self):

        # for self.kd in self.kds:
        #
        #     scrapy.http.FormRequest(self.myurl,
        #                                 formdata={'pn':str(self.curpage),'kd':self.kd},callback=self.parse)

        # 查询特定关键词的内容，通过request
        return [
            scrapy.http.FormRequest(self.myurl, formdata={'first':'true','pn': str(self.curpage), 'kd': self.kd}, callback=self.parse,
                                    headers=self.HEADER)]

    def parse(self, response):
        print response.body
        fp = open('1.html', 'wb')
        fp.write(response.body)
        item = LagouItem()
        jdict = json.loads(response.body)
        jcontent = jdict['content']
        jposresult = jcontent['positionResult']
        jresult = jposresult['result']

        # 计算总页数
        self.totalPageCount = jposresult['totalCount'] / 15 + 1;
        if self.totalPageCount > 30:
            self.totalPageCount = 30;

        for each in jresult:
            item['city'] = each['city']
            item['companyName'] = each['companyName']
            item['companySize'] = each['companySize']
            item['positionName'] = each['positionName']
            item['positionType'] = each['positionType']
            sal = each['salary']
            sal = sal.split('-')
            if len(sal) == 1:
                item['salaryMax'] = int(sal[0][:sal[0].find('k')])
            else:
                item['salaryMax'] = int(sal[1][:sal[1].find('k')])

            item['salaryMin'] = int(sal[0][:sal[0].find('k')])
            item['salaryAvg'] = (item['salaryMin'] + item['salaryMax']) / 2
            item['positionAdvantage'] = each['positionAdvantage']
            item['companyLabelList'] = each['companyLabelList']
            item['keyword'] = self.kd
            yield item
        if self.curpage <= self.totalPageCount:
            self.curpage += 1
            yield scrapy.http.FormRequest(self.myurl, formdata={'pn': str(self.curpage), 'kd': self.kd},
                                          callback=self.parse, headers=self.HEADER)
        elif self.cur < len(self.kds) - 1:
            self.curpage = 1
            self.totalPageCount = 0
            self.cur += 1
            self.kd = self.kds[self.cur]
            yield scrapy.http.FormRequest(self.myurl, formdata={'pn': str(self.curpage), 'kd': self.kd},
                                          callback=self.parse, headers=self.HEADER)
