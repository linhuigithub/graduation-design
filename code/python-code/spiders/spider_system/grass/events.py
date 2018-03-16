import collections
import logging
import threading
from collections import Counter

import asyncio

import time

import celery
from celery.events import EventReceiver
from celery.events.state import State

logger = logging.getLogger(__name__)


class EventsState(State):
    def __init__(self, *args, **kwargs):
        super(EventsState, self).__init__(*args, **kwargs)
        self.counter = collections.defaultdict(Counter)

    def event(self, event):
        worker_name = event['hostname']
        event_type = event['type']

        self.counter[worker_name][event_type] += 1
        # Save the event
        super(EventsState, self).event(event)


class Events(threading.Thread):
    events_enable_interval = 5000

    def __init__(self, capp, loop=None, **kwargs):
        threading.Thread.__init__(self)
        self.daemon = True  # 设置成守护线程，主线程停止，子线程也会停止（其实线程没有主线程，子线程的区分，这里只是借用了一下概念方便描述）

        # self.loop = loop or asyncio.get_event_loop()
        self.capp = capp  # type: celery.Celery
        self.state = EventsState(**kwargs)

    def start(self):
        super(Events, self).start()
        self.on_enable_events()
        # start periodic enable_events

    def run(self):
        try_interval = 1
        while True:
            try:
                try_interval *= 2

                with self.capp.connection() as conn:
                    recv = EventReceiver(
                        conn,
                        handlers={'*': self.on_event},
                        app=self.capp)
                    try_interval = 1
                    recv.capture(limit=None, timeout=None, wakeup=True)
            except (KeyboardInterrupt, SystemExit):
                import _thread as thread
                thread.interrupt_main()
            except Exception as e:
                logger.error('捕获 Celery 事件失败: "%s". '
                             '将在 %s 秒后重试...', e, try_interval)
                logger.debug(e, exc_info=True)
                time.sleep(try_interval)

    def on_enable_events(self):
        """
        启动celery事件

        :return:
        """
        try:
            self.capp.control.enable_events()
        except Exception as e:
            logger.debug('启动 Celery 事件失败: "%s"', e)

    def on_event(self, event):
        # TODO: 异步调用 event
        self.state.event(event)
