# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst, Join
from w3lib.html import remove_tags


class LagouItem(scrapy.Item):
    _id = scrapy.Field()
    from_website = scrapy.Field()
    min_salary = scrapy.Field()
    max_salary = scrapy.Field()
    location = scrapy.Field()
    publish_date = scrapy.Field()
    work_type = scrapy.Field()
    work_experience = scrapy.Field()
    limit_degree = scrapy.Field()
    people_count = scrapy.Field()
    work_name = scrapy.Field()
    work_duty = scrapy.Field()
    work_need = scrapy.Field()
    work_content = scrapy.Field()
    work_info_url = scrapy.Field()
    business_name = scrapy.Field()
    business_type = scrapy.Field()
    business_count = scrapy.Field()
    business_website = scrapy.Field()
    business_industry = scrapy.Field()
    business_location = scrapy.Field()
    business_info = scrapy.Field()


# class LagouJobItem(scrapy.Item):
#     url = scrapy.Field()
#     experience = scrapy.Field()
#     education = scrapy.Field()
#     occupation_temptation = scrapy.Field()
#     job_fields = scrapy.Field()
#     stage = scrapy.Field()
#     scale = scrapy.Field()
#     title = scrapy.Field()
#     url_obj_id = scrapy.Field()
#     salary = scrapy.Field()
#     job_city = scrapy.Field(
#         input_processor=MapCompose(replace_splash)
#     )
#     work_years = scrapy.Field(
#         input_processor=MapCompose(replace_splash)
#     )
#     degree_need = scrapy.Field(
#         input_processor=MapCompose(replace_splash)
#     )
#     job_type = scrapy.Field()
#     publish_time = scrapy.Field()
#     tags = scrapy.Field(
#         input_processor=Join(',')
#     )
#     job_advantage = scrapy.Field()
#     job_desc = scrapy.Field(
#         # 移除html标签
#         input_processor=MapCompose(remove_tags)
#     )
#     job_addr = scrapy.Field(
#         input_processor=MapCompose(remove_tags, handle_jobaddr)
#     )
#     company_url = scrapy.Field()
#     company_name = scrapy.Field()
#     company = scrapy.Field()
#     founder = scrapy.Field()
#     craw_time = scrapy.Field()
#     craw_update_time = scrapy.Field()
#
#     # 重写get_insert_sql方法，该方法会在MyTwistedPipeline中调用，执行存储操作，ON DUPLICATE KEY UPDATE 表示如果主键冲突，则不进行插入操作，执行更新职位描述操作
#     def get_insert_sql(self):
#         insert_sql = """
#                 insert into lagou_table(url, url_obj_id, title, salary, job_city,
#                     work_years, degree_need, job_type, publish_time, tags, job_advantage,
#                     job_desc, job_addr, company_url, company_name
#                 ) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE job_desc=VALUES(job_desc)
#             """
#
#         params = (
#             self['url'], self['url_obj_id'], self['title'], self['salary'], self['job_city'],
#             self['work_years'], self['degree_need'], self['job_type'], self['publish_time'],
#             self['tags'], self['job_advantage'], self['job_desc'], self['job_addr'],
#             self['company_url'], self['company_name']
#         )
#         return insert_sql, params
