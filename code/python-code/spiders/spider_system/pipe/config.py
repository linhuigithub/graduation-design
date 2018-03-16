import os
import pymongo

from dotenv import find_dotenv, load_dotenv

# 加载 dotenv 文件
load_dotenv(find_dotenv())

# 加载配置
config = {
    # mongodb 配置（爬虫数据库）
    "mongo": {
        "host": os.getenv("MONGO_HOST", "localhost"),
        "port": int(os.getenv("MONGO_PORT", "27017")),
        # "auth_db": os.getenv("MONGO_AUTH_DB"),
        "database": os.getenv("MONGO_DATABASE", "demo"),
        "collection": os.getenv("MONGO_COLLECTION", "demo"),
        "username": os.getenv("MONGO_AUTH_USER", ""),
        "password": os.getenv("MONGO_AUTH_PASS", ""),
    },
}


def create_mongo():
    client = pymongo.MongoClient(host=config['mongo']['host'], port=config['mongo']['port'])
    db = client[config['mongo']['database']]
    collection = db[config['mongo']['collection']]
    return collection


if __name__ == '__main__':
    create_mongo()
