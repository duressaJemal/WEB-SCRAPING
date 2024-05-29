# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import logging
import pymongo
import os

from dotenv import load_dotenv
from itemadapter import ItemAdapter


load_dotenv

class MongoDBPipeline:

    CLIENT = os.getenv("MONGO_CLIENT")
    collection_name = "transcripts"
    database_name = "My_DB"


    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.CLIENT)
        self.db = self.client[self.database_name]
        logging.warning("Spider opened from pipeline")

    def close_spider(self, spider):
        self.client.close()
        logging.warning("Spider closed from pipeline")

    def process_item(self, item, spider):
        self.db[self.collection_name].insert_one(item)
        return item


