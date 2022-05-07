# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import json

from itemadapter import ItemAdapter

from jsonschema import Draft7Validator
from json import load


class SiteScrapingPipeline:
    def __init__(self):
        pass

    def process_item(self, item, spider):
        self.json_validate(dict(item))
        return item

    def json_validate(self, item):
        with open("schema.json") as f:
            schema = load(f)

        validator = Draft7Validator(schema)
        print(list(validator.iter_errors(item)))
