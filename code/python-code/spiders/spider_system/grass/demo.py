import celery
import time

from requests import HTTPError

from spider_system.grass.config import create_celery_app
from spider_system.grass.events import Events
from spider_system.grass import tasks
from spider_system.grass.monitor import abort_task, revoke_task

# capp = celery.Celery('tasks', broker='redis://localhost:6379/1')
capp = create_celery_app('tasks')
events = Events(capp)
events.start()


def get_task_info(events, taskid):
    task = tasks.get_task_by_id(events, taskid)
    if not tasks:
        raise HTTPError(404, "Unknown task '%s'" % taskid)
    response = task.as_dict()
    if task.worker is not None:
        response['worker'] = task.worker.hostname
    print(response)


while True:
    time.sleep(1)
    tasks = list()
    for uuid, task in events.state.tasks.items():
        task_message = dict()
        # uuid
        task_message['uuid'] = uuid
        # 名称
        task_name = task.name
        task_message['task_name'] = task_name
        # 状态
        task_state = task.state
        task_message['task_state'] = task_state
        # 发送时间
        task_received = task.received
        task_message['task_received'] = task_received
        # 启动时间
        task_started = task.started
        task_message['task_started'] = task_started
        # 完成时间
        task_succeeded = task.succeeded
        task_message['task_succeeded'] = task_succeeded
        # worker
        worker = task.worker.hostname
        task_message['worker'] = worker
        # 耗时
        clock = task.clock
        task_message['clock'] = clock
        # 结果
        result = task.result
        task_message['result'] = result
        tasks.append(task_message)
        # get_task_info(events, uuid)
        # revoke_task(capp, uuid)
        # abort_task(uuid)
    print(len(tasks))
