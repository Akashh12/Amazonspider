# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class AmazonxItem(scrapy.Item):
    # define the fields for your item here like:
    link = scrapy.Field()
    product_name = scrapy.Field()
    mobile_name = scrapy.Field()
    mobile_price = scrapy.Field()
    customer_rating = scrapy.Field()
    pass
