import requests


def run():
    yield requests.get('http://www.baidu.com').status_code


for i in run():
    print(i)
