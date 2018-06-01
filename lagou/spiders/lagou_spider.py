# -*- coding: utf-8 -*-
import scrapy
import logging
from scrapy import Request
from lagou.items import LagouItem
import json

logger = logging.getLogger('jintao')


class LagouSpiderSpider(scrapy.Spider):
    name = 'lagou'
    allowed_domains = ['lagou.com']

    kd = '会计'
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Cookie': '_ga=GA1.2.1675705296.1525503483; user_trace_token=20180505145804-a854ed80-5031-11e8-869c-525400f775ce; LGUID=20180505145804-a854f0b2-5031-11e8-869c-525400f775ce; _gid=GA1.2.1639933130.1525856914; index_location_city=%E6%B7%B1%E5%9C%B3; JSESSIONID=ABAAABAACEBACDG04FABB7BD87B79FAC311DCA849B647AD; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1525503484,1525869827; X_HTTP_TOKEN=a182ed869a8003910c5f297e88d8d0ce; X_MIDDLE_TOKEN=08efdfbc4e46f32d79b4965ed35ed919; LGSID=20180510142346-b222b4ee-541a-11e8-81e3-5254005c3644; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1525938024; LGRID=20180510154024-663ed077-5425-11e8-93e9-525400f775ce; TG-TRACK-CODE=search_code; SEARCH_ID=be579ebfc13249c4b2dfbcef8a093f71',
        'Host': 'www.lagou.com',
        'Origin': 'https://www.lagou.com',
        'Referer': 'https://www.lagou.com/jobs/list_python?labelWords=&fromSearch=true&suginput=',
        'User-Agent': 'User-Agent:Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
        'X-Anit-Forge-Code': '0',
        'X-Anit-Forge-Token': 'None',
        'X-Requested-With': 'XMLHttpRequest'}

    def start_requests(self):
        url = 'https://www.lagou.com/jobs/positionAjax.json?city=%E6%B7%B1%E5%9C%B3&needAddtionalResult=false'
        yield scrapy.FormRequest(url, formdata={'first': 'true', 'pn': '1', 'kd': self.kd}, method='Post',
                                 meta={'pn': 1}, headers=self.headers, callback=self.parse)

    def parse(self, response):
        print(response.url)
        html = response.text
        data = json.loads(html)
        if data:
            content = data.get('content')
            positionResult = content.get('positionResult')
            totalCount = positionResult.get('totalCount')
            pages = int(totalCount / 3)
            if pages >= 30:
                pages = 30
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
                yield item

            pn = int(response.meta.get('pn')) + 1
            if pn <= pages:
                yield scrapy.FormRequest(response.url, formdata={'first': 'False', 'pn': str(pn), 'kd': self.kd},
                                         method='Post', meta={'pn': pn}, headers=self.headers, callback=self.parse)
