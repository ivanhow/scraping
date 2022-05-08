# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import json

from itemadapter import ItemAdapter

from jsonschema import Draft7Validator
from json import load
import sqlite3


class SiteScrapingPipeline:
    def __init__(self):
        self.create_connection()
        self.create_table()

    def create_connection(self):
        self.conn = sqlite3.connect('mydatabase.db')
        self.curr = self.conn.cursor()

    def create_table(self):
        self.curr.execute("""create table if not exists data_tb(
                        date text,
                        notice_number text PRIMARY KEY,
                        tender_name text,
                        procedure_state text,
                        contract_type text,
                        type_of_procurement text,
                        estimated_value text 
                        )""")

    def process_item(self, item, spider):
        self.store_db(item)
        self.json_validate(dict(item))

        return item

    def json_validate(self, item):
        with open('schema.json') as f:
            schema = load(f)

        validator = Draft7Validator(schema)
        print(list(validator.iter_errors(item)))

    def store_db(self, items):
        self.curr.execute("""INSERT OR IGNORE INTO data_tb VALUES (?,?,?,?,?,?,?)""", (
            items['date'],
            items['notice_number'],
            items['tender_name'],
            items['procedure_state'],
            items['contract_type'],
            items['type_of_procurement'],
            items['estimated_value']
        ))
        self.conn.commit()

