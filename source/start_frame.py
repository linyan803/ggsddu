#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
GGSDDU 的启动程序
1. git 主目录
2. 获取当前登录用户名，当前登录用户名即数据库文件名
3. 检查数据库文件如果不存在，那么创建数据库文件
4. 读取history.list中最后一行的日期, 没有即为0
5. 将PERSONAL.db中晚于上面日期的条目插入到新建数据库中
"""

import os

import sqlite3
import platform

from tkinter import Tk, Text, Scrollbar
from tkinter import RIGHT, Y, END
from tkinter.font import Font

SCRIPT_PATH = os.path.dirname(os.path.abspath(__file__))


class StartWindow:
    def __init__(self, the_root, font_name):
        self.root = the_root
        self.my_font = Font(family=font_name, size=12)  # 部分按钮字体小一点
        self.show_text = Text(
            self.root,
            font=self.my_font
        )

        self.scroll = Scrollbar()
        # 放到窗口的右侧, 填充Y竖直方向
        self.scroll.pack(side=RIGHT, fill=Y)

        # 两个控件关联
        self.scroll.config(command=self.show_text.yview)
        self.show_text.config(yscrollcommand=self.scroll.set)
        self.show_text.pack()

        self.git_ggsddu()

    def git_ggsddu(self):
        result = os.popen('git pull')
        responses = result.read()
        for line in responses.splitlines():
            self.show_text.insert(END, line+'\n')


if __name__ == '__main__':
    # 创建主窗口
    root = Tk()
    root.title('The notebook of wrong questions for Li Zhenzhen')

    system_name = platform.system()
    # print(system_name)
    if 'Windows' in system_name:
        FONT_NAME = '微软雅黑'
    elif 'Linux' in system_name:
        FONT_NAME = 'Century Schoolbook L'
    else:
        print('Can only support windows and linux')

    width = 600
    height = 400
    screenwidth = root.winfo_screenwidth()
    screenheight = root.winfo_screenheight()
    root.geometry('%dx%d+%d+%d' %
                  (width, height,
                   (screenwidth-width)/2,
                   (screenheight-height)/2))
    root.resizable(0, 0)  # 防止用户调整尺寸

    # 建立App
    app = StartWindow(root, FONT_NAME)

    # personal_conn = sqlite3.connect(SCRIPT_PATH+"/../database/LIZHENZHEN.db")
    # personal_cur = personal_conn.cursor()

    # 进入消息循环
    root.mainloop()
