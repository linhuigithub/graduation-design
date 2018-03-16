import requests

from spider_system.log import log

logging = log.Log(__file__, 'request').logger


def get(url, headers=None, timeout=15, retry=2):
    while retry > 0:
        try:
            res = requests.get(url, headers=headers, timeout=timeout)
            return res.text
        except Exception as e:
            logging.info('{}: {}'.format(url, e))
        retry -= 1


def post(url, data=None, headers=None, timeout=15, retry=2):
    while retry > 0:
        try:
            res = requests.post(url, data=data, headers=headers, timeout=timeout)
            return res.text
        except Exception as e:
            logging.info('{}: {}'.format(url, e))
        retry -= 1
