#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
全局日志模块
"""
import logging
import os

SCRIPT_PATH = os.path.dirname(os.path.abspath(__file__))
# ggsddu/source/misc/
LOG_FORMAT = '%(asctime)s %(filename)s[line:%(lineno)d]"' \
             '" %(levelname)s:  %(message)s'


class Log:
    # 初始化日志
    def __init__(self):
        self.name = "ggsddu"
        log_path = SCRIPT_PATH + "/../../logs"
        log_file_name = self.name + '.log'
        self.log_file = log_path + '/' + log_file_name
        # 日志的输出格式
        logging.basicConfig(
            level=logging.INFO,
            # 级别：CRITICAL > ERROR > WARNING > INFO > DEBUG，默认级别为 WARNING
            format=LOG_FORMAT,
            datefmt='%Y-%m-%d %H:%M:%S',
            filename=self.log_file,
            filemode='a')

    @staticmethod
    def _log_with_level(string, level):
        # 只支持info和error
        if logging.INFO == level:
            logging.info(string)
        if logging.ERROR == level:
            logging.error(string)

    def _split_type(self, content, level):
        # 能处理 字符串，tuple，list三种
        if isinstance(content, str):
            # print("I am string")
            self._log_with_level(content, level)
        if isinstance(content, tuple):
            # print("I am tuple")
            all_text = ''
            for item in content:
                all_text += str(item) + ', '
            all_text = all_text[:-2] + '\n'
            # print(all_text)
            self._log_with_level(all_text, level)

        if isinstance(content, list):
            # print("I am list")
            for line in content:
                self._log_with_level(line, level)

    def info(self, content):
        if len(content) > 0:
            self._split_type(content, logging.INFO)
        else:
            print("log info empty")

    def error(self, content):
        if len(content) > 0:
            self._split_type(content, logging.ERROR)
        else:
            print("log error empty")


if __name__ == '__main__':
    # 测试代码
    my_log = Log()
    res = os.popen("dir")
    my_log.info(res.read().splitlines())

    one_string = "I am single string"
    my_log.error(one_string)

    my_log.error((1, 2, 3, 4, 5))

