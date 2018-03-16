"""
WSGI config for spider_system project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/howto/deployment/wsgi/
"""

import os

import time
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "spider_system.settings")

application = get_wsgi_application()

import threading

lock = threading.Lock()
flag = 0


class ThreadOne(threading.Thread):
    def __init__(self):
        super().__init__()

    def run(self):
        global flag
        while 1:
            if flag == 0:
                lock.acquire()
                print('producer...')
                flag = 1


class ThreadTwo(threading.Thread):
    def __init__(self):
        super().__init__()
        # self.daemon = True

    def run(self):
        global flag
        while 1:
            if flag == 1:
                lock.release()
                print('consumer...')
                flag = 0


if __name__ == '__main__':
    t1 = ThreadOne()
    t2 = ThreadTwo()
    t1.start()
    t2.start()
