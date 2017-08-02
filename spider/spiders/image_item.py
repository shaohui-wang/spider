import scrapy


class ImageItem(scrapy.Item):
    name = scrapy.Field()
    src = scrapy.Field()
