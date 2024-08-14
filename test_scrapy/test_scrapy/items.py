# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class OfficeScraperItem(scrapy.Item):
    name = scrapy.Field()
    link = scrapy.Field()

# class TestScrapyItem(scrapy.Item):
#     # define the fields for your item here like:
#     name = scrapy.Field()
#     link = scrapy.Field()
#     # image = scrapy.Field()
#     # description = scrapy.Field()
#     pass

