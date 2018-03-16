import threading
import time
from lxml import etree

from spider_system.crawlfile.reader import read_file
from spider_system.grass.config import create_celery_app
from spider_system.kumo import request

from spider_system.log.log import Log
from spider_system.utils.request import get, post

logging = Log(__file__, 'spider_tasks').logger

capp = create_celery_app('tasks')


@capp.task
def get_message_by_xpath(url, file_name):
    """
    通过xpath获取信息

    :param url:
    :param file_name:
    :return:
    """
    crawle_rules = read_file(file_name)
    result = request.get_by_xpath(url, crawle_rules)
    return result


@capp.task
def subtask_by_xpath(target_url, rule_list, done_target_url_list, will_do_target_url_list):
    """

    :param target_url:
    :param rule_list:
    :param done_target_url_list:
    :param will_do_target_url_list:
    :return:
    """
    html = get(target_url)
    try:
        tree = etree.HTML(html)
    except Exception as e:
        print(e, target_url)
        return

    result = dict()
    for item in rule_list:
        title = item[0]
        path = item[1]
        content = tree.xpath(path)

        # 将新获取到的url添加到待爬取列表中
        if title == 'target_url_rule':
            for url in content:
                # 进行一次简单的去重
                if url not in done_target_url_list:
                    done_target_url_list.append(url)
                    will_do_target_url_list.append(url)
                    print('目前列表长度：', len(will_do_target_url_list))
        result[title] = content
    print(result)


# 实现给一个入口url， 全网爬的功能，但是python不支持闭包序列化，还不能用回调实现
@capp.task
def crawler_full_network_by_xpath(seed_url, rule_file):
    """

    :param seed_url:
    :param rule_file:
    :return:
    :explain: 通过seed_url，获取到 target_url;然后再把target_url以任务的形式下发
    """

    '''
    1.根据seed_url获取到target_url列表
    2.调用具体抓取任务，将target_url传递给抓取任务，同时，抓取任务也会更多的向target_url列表中添加url，在列表中去重，再分发给任务
    3.第二步需要多线程实现,线程一实现任务的分发；线程二实现具体任务的抓取和新添加target_url到target_url列表的功能
    '''

    thread_task = ThreadTask(rule_file=rule_file, seed_url=seed_url)
    thread_task.start()


class ThreadTargetUrl(threading.Thread):
    def __init__(self, seed_url):
        super(ThreadTargetUrl, self).__init__(self)
        self.seed_url = seed_url
        self.done_target_url_list = list()
        self.will_do_arget_url_list = list()

    def start(self):
        super(ThreadTargetUrl, self).start()

    def run(self):
        target_urls = request.get_by_xpath(self.seed_url, 'xpath')
        for target_url in target_urls:
            # 验证target_url的合法性
            if target_url not in self.done_target_url_list:
                self.done_target_url_list.append(target_url)
                self.will_do_arget_url_list.append(target_url)


class ThreadTask(threading.Thread):
    """
    爬取规则里面包含爬取具体内容的规则， 爬取targrt_url的规则
    """

    def __init__(self, seed_url, rule_file):
        super(ThreadTask, self).__init__()
        self.seed_url = seed_url

        self.done_target_url_list = list()
        self.will_do_arget_url_list = list()

        self.rule_list = read_file(rule_file)

    def start(self):

        # 根据种子获取target_url,并将其添加到target_url列表中
        """
        code:

        """

        html = get(self.seed_url)
        tree = etree.HTML(html)
        target_url_list = tree.xpath(self.rule_list[0][1])

        if not target_url_list:
            logging.info('seed_url，或target_url_rule错误，无法解析到链接')
            return

        for target_url in target_url_list:
            self.will_do_arget_url_list.append(target_url)
        super(ThreadTask, self).start()

    def run(self):
        """

        :return:

        1.线程等待是否应该放在这里？
        2.任务线程的终止条件是什么？
        """
        while True:
            if self.will_do_arget_url_list:

                # 爬取待爬列表的内容(这里调用任务，以子任务的形式执行)
                target_url = self.will_do_arget_url_list[0]
                self.will_do_arget_url_list.pop(0)

                '''
                task_code
                1.要验证url的合法性，否则爬虫会进行不下去,需要精准的验证，目前这里只是排除
                '''
                if target_url.find('http') == -1:
                    logging.info('target_url: {}  --不合法'.format(target_url))
                    continue

                subtask_by_xpath.delay(
                    target_url,
                    self.rule_list,
                    self.done_target_url_list,
                    self.will_do_arget_url_list
                )

            else:
                logging.info('target_url列表已空')
                time.sleep(10)

    def request_and_parse(self, url, parse_rule):
        pass


if __name__ == '__main__':
    crawler_full_network_by_xpath('http://www.baidu.com', 'demo.txt')
