# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class SiteScrapingItem(scrapy.Item):
    # define the fields for your item here like:
    date = scrapy.Field()
    notice_number = scrapy.Field()
    tender_name = scrapy.Field()
    procedure_state = scrapy.Field()
    contract_type = scrapy.Field()
    type_of_procurement = scrapy.Field()
    estimated_value = scrapy.Field()
