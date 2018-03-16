# 爬取信息文件读取器，其作用是将爬取信息读入列表，并整理为工具可识别的格式
import re
import os


def read_file(file_name):
    path = os.path.abspath(__file__).replace('reader.py', '')
    with open(path + file_name, 'r') as f:
        rule_list = list()
        for item in f.readlines():
            item = re.sub('\s', '', item)
            if item:
                item = item.split('=')
                rule_list.append(item)
        return rule_list


def deal_regular():
    # 处理成为 正则， xpath， css选择器等可以识别并处理的标准格式
    pass


if __name__ == '__main__':
    print(read_file('demo.txt'))
