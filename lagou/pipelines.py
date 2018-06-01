# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import codecs
from scrapy.exporters import JsonItemExporter

class JsonWriterPipeline(object):
    def __init__(self):
        self.file = codecs.open('items.json', 'w', encoding='utf-8')
        # self.exporter = JsonItemExporter(self.file, encoding='utf-8')
        # self.exporter.start_exporting()

    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=False) + '\n'
        self.file.write(line)
        # self.exporter.export_item(item)
        return item

    def spider_closed(self, spider):
        # self.exporter.finish_exporting()

        self.file.close()

