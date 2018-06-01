# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Field, Item


class LagouItem(Item):
    companyFullName = Field()
    companyId = Field()
    companyLabelList = Field()
    companyLogo = Field()
    companyShortName = Field()
    companySize = Field()
    createTime = Field()
    deliver = Field()
    district = Field()
    education = Field()
    explain = Field()
    financeStage = Field()
    firstType = Field()
    formatCreateTime = Field()
    gradeDescription = Field()
    industryField = Field()
    industryLables = Field()
    isSchoolJob = Field()
    jobNature = Field()
    positionAdvantage = Field()
    positionId = Field()
    positionLables = Field()
    positionName = Field()
    salary = Field()
    secondType = Field()
    workYear = Field()
    totalCount = Field()

