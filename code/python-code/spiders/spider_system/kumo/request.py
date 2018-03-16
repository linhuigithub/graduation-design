from lxml import etree
from spider_system.crawlfile.reader import read_file
from spider_system.utils.request import get
from spider_system.utils.xpath import path_one, path_many


def get_by_xpath(url, crawle_rules):
    """

    :param url:
    :param crawle_rules:
    :return:

    通过xpath获取信息
    """
    res = get(url)
    tree = etree.HTML(res)
    result = dict()
    for crawle_rule in crawle_rules:
        key = crawle_rule[0]
        rule = crawle_rule[1]
        result[key] = path_one(tree, rule, delete_space=False)
    return result


def get_by_re(url, crawle_rules):
    """

    :param url:
    :param crawle_rules:
    :return:

    通过正则表达式获取信息
    """
    pass


def get_by_css(url, crawler_rules):
    """

    :param url:
    :param crawler_rules:
    :return:

    通过css选择器获取信息
    """
    pass


if __name__ == '__main__':
    crawle_rules = read_file('demo.txt')
    get_by_xpath('http://python.jobbole.com/87310/', crawle_rules)
