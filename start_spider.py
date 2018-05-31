# -*- coding: utf-8 -*-


import os
import sys
from schedule import Scheduler
from twisted.internet import reactor
from pydispatch import dispatcher

from scrapy.crawler import CrawlerProcess
from scrapy.conf import get_project_settings
from scrapy import signals

from lagou.spiders.lagouSpider import LagouSpider
from lagou.logger.LoggerHandler import Logger

# 日志中心
# logger = Logger(logger='start_spider.py').get_logger()

path = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
sys.path.append(path)


class Runner(object):
    def __init__(self, name):
        # 是否启动
        self.is_running = False
        # 连接spider engine
        dispatcher.connect(self.pause_crawler, signals.engine_stopped)
        # 获取scrapy设置
        self.setting = get_project_settings()
        # 进程数
        self.process = None
        # 爬虫参数
        self._name = name

    def start_scrapy(self):
        self.process = CrawlerProcess(self.setting)
        self.crawl()
        reactor.run()

    def pause_crawler(self):
        self.is_running = False
        print("============= stop停止 ===============").encode('gbk')
        sys.exit(1)

    def crawl(self):
        self.is_running = True
        self.process.crawl(LagouSpider, search_name=self._name)

    def run(self):
        self.start_scrapy()



if __name__ == '__main__':
    input_res = sys.argv[1].split("=")

    if input_res[0] == "-name":
        if input_res[1] == "" or input_res[1] is None:
            sys.exit(1)
        else:
            runner = Runner(name=input_res[1])

            def task():
                if not runner.is_running:
                    print("=========== begin ==========").encode('gbk')
                    runner.crawl()

            # schedule = Scheduler()
            # schedule.every().days.at("01:00").do(task)

            runner.run()