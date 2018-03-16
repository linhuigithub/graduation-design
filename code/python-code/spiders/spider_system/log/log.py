import os

local_path = os.path.abspath(__file__).replace('log.py', '')

import logging


class Log(object):
    def __init__(self, log_name, log_file):
        self.logger = logging.getLogger(log_name)
        self.logger.setLevel(logging.INFO)
        logdir_path = '{}{}{}'.format(local_path, 'logdir/', log_file)
        self.mkdir(logdir_path)
        logfile = logging.FileHandler('{}{}{}.log'.format(logdir_path, '/', log_file))
        logfile.setLevel(logging.INFO)

        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        logfile.setFormatter(formatter)

        self.logger.addHandler(logfile)

    def mkdir(self, path):
        is_exists = os.path.exists(path)
        if not is_exists:
            os.mkdir(path)
