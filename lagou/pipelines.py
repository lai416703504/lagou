# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from twisted.enterprise import adbapi
# import MySQLdb.cursors
# import MySQLdb
import csv


class LagouPipeline(object):
    def __init__(self):
        # csv文件的位置，无需实现创建
        store_file = 'lagou.csv'
        # 打开(创建)文件
        self.file = open(store_file, 'wb')
        # CSV写法
        self.writer = csv.writer(self.file)

    def process_item(self, item, spider):
        self.writer.writerow((item['salary'].encode('utf8', 'ignore'), item['experience'].encode('utf8', 'ignore'),
                              item['education'].encode('utf8', 'ignore'),
                              item['occupation_temptation'].encode('utf8', 'ignore'),
                              item['job_fields'].encode('utf8', 'ignore'), item['stage'].encode('utf8', 'ignore'),
                              item['scale'].encode('utf8', 'ignore'), item['company'].encode('utf8', 'ignore'),
                              item['url'].encode('utf8', 'ignore'), item['founder'].encode('utf8', 'ignore')))

        return item

    def close_spider(self, spider):
        # 关闭爬虫时顺便将文件保存退出
        self.file.close()


class MyTwistedPipeline(object):
    pass
    # def __init__(self, dbpool):
    #     # 在执行完from_settings之后,将dbpool初始化
    #     self.dbpool = dbpool
    #
    # @classmethod
    # def from_settings(cls, settings):
    #     dbparams = dict(
    #         host=settings["MYSQL_HOST"],
    #         port=settings["MYSQL_PORT"],
    #         user=settings["MYSQL_USER"],
    #         passwd=settings["MYSQL_PWD"],
    #         db=settings["MYSQL_DB"],
    #         charset=settings["MYSQL_CHARSET"],
    #         use_unicode=settings["MYSQL_USER_UNICODE"],
    #         cursorclass=MySQLdb.cursors.DictCursor,
    #     )
    #     # 这里通过adbapi构造一个dbpool，并传入MyTwistedPipeline的构造方法
    #     dbpool = adbapi.ConnectionPool("MySQLdb", **dbparams)
    #     return cls(dbpool)
    #
    # def process_item(self, item, spider):
    #     # 使用twisted异步插入数据到mysql
    #     query = self.dbpool.runInteraction(self.insert_data, item)
    #     query.addErrback(self.handle_error)
    #
    # def handle_error(self,failure):
    #     # 处理异步插入异常
    #     print(failure)
    #
    # def insert_data(self, cursor, item):
    #     # 执行具体的插入
    #     # 根据不同的item 构建不同的sql语句并插入到mysql中
    #     insert_sql, params = item.get_insert_sql()
    #     print(insert_sql, params)
    #     cursor.execute(insert_sql, params)
