import re


def path_one(tree, path, delete_space=True):
    result = tree.xpath(path)
    if result:
        if delete_space:
            result = re.sub('\s', '', result[0])
        else:
            result = result[0].strip()
        return result


def path_many(tree, path, delete_space=True):
    results = tree.xpath(path)
    if results:
        message_list = list()
        if delete_space:
            for item in results:
                result = re.sub('\s', '', item)
                message_list.append(result)
        else:
            for item in results:
                result = item.strip()
                message_list.append(result)
