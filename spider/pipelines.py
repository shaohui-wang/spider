# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os

import requests

from spider import settings


class SpiderPipeline(object):
    def process_item(self, item, spider):
        if 'src' in item:
            dir_path = '%s/%s' % (settings.IMAGES_STORE, spider.name)
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)
            for image_url in item['src']:
                suffix = image_url.split('.')[-1]
                file_path = '%s/%s.%s' % (dir_path, item['name'], suffix)
                if os.path.exists(file_path):
                    continue
                with open(file_path, 'wb') as handle:
                    response = requests.get(image_url, stream=True)
                    for block in response.iter_content(1024):
                        if not block:
                            break
                        handle.write(block)
        return item
