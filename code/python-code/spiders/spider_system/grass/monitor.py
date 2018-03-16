'''
监控的内容
'''

import celery
import time

from celery.contrib.abortable import AbortableAsyncResult
from requests import HTTPError

from spider_system.grass.config import create_celery_app
from spider_system.grass.events import Events
from spider_system.grass import tasks

capp = create_celery_app('tasks')

events = Events(capp)
events.start()


# 获取指定任务的信息（通过uuid）
def get_task_info(events, taskid):
    task = tasks.get_task_by_id(events, taskid)
    if not tasks:
        raise HTTPError(404, "Unknown task '%s'" % taskid)
    response = task.as_dict()
    if task.worker is not None:
        response['worker'] = task.worker.hostname
    return response


# 获取全部任务
def get_tasks(events):
    for uuid, task in events.state.tasks.items():
        yield uuid, task


# 终止指定任务
def abort_task(taskid):
    result = AbortableAsyncResult(taskid)
    result.abort()


# 撤销指定任务
def revoke_task(capp, taskid):
    capp.control.revoke(taskid)


if __name__ == '__main__':
    for item in get_tasks(events):
        print(item)
