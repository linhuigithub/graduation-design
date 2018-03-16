import os

from celery import Celery
from dotenv import find_dotenv, load_dotenv

# 加载 dotenv 文件
load_dotenv(find_dotenv())

__all__ = ["config", "create_celery_app"]

# 加载配置
config = {
    # mongodb 配置（后端数据库）
    "mongo": {
        "host": os.getenv("MONGO_HOST", "localhost"),
        "port": int(os.getenv("MONGO_PORT", "27017")),
        # "auth_db": os.getenv("MONGO_AUTH_DB"),
        "database": os.getenv("MONGO_DATABASE"),
        "username": os.getenv("MONGO_AUTH_USER", ""),
        "password": os.getenv("MONGO_AUTH_PASS", ""),
    },
    # redis 配置（消息队列）
    "redis": {
        "host": os.getenv("REDIS_HOST", "localhost"),
        "port": int(os.getenv("REDIS_PORT", "6379")),
        # "username": os.getenv("REDIS_USER", ""),
        # "password": os.getenv("REDIS_PASS", ""),
    }
}


def create_celery_app(name, broker=None, backend=None):
    if broker is None:
        broker = "redis://{host}:{port}/1".format(**config["redis"])
    if backend is None:
        backend = "mongodb://{host}:{port}/{database}".format(**config["mongo"])
    return Celery(main=name, broker=broker, backend=backend)
