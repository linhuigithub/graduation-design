import pymongo

from spider_system.pipe.config import create_mongo


class MongoDB(object):
    def __init__(self):
        self.mongo = create_mongo()

    # 如果主键相同，会报错
    def put(self, value):
        self.mongo.insert(value)

    # 主键相同，会覆盖掉之前的数据
    def save(self, value):
        self.mongo.save(value)

    def get(self, **kwargs):
        self.mongo.find(kwargs)

    def get_one(self):
        self.mongo.find_one()
