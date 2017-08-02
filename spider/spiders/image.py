# -*- coding: utf-8 -*-
import scrapy
from scrapy import Selector, Request
from scrapy.loader import ItemLoader, Identity

from spider.spiders.image_item import ImageItem


class FlightSpider(scrapy.Spider):
    name = 'mm131'
    allowed_domains = ["mm131.com"]
    start_urls = [
        'http://www.mm131.com/xinggan/3072.html',
    ]

    def parse(self, response):
        yield self.parse_item(response)
        # 获得分页的链接
        selector = Selector(response)
        next_page = selector.xpath(
            '//div[@class="content-page"]/span[@class="page_now"]/following-sibling::*[1]/@href').extract()

        if len(next_page) == 1:
            url = 'http://www.mm131.com/xinggan/' + next_page[0]
            print(url)
            yield Request(url, callback=self.parse)

    def parse_item(self, response):
        l = ItemLoader(item=ImageItem(), response=response)
        print(response.xpath('//div[@class="content-pic"]/a/img/@alt'))
        l.add_xpath('name', '//div[@class="content-pic"]/a/img/@alt')
        l.add_xpath('src', '//div[@class="content-pic"]/a/img/@src', Identity())
        return l.load_item()
