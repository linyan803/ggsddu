#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import sys

# 为了引入工程/source目录中的模块
THIS_PATH= os.path.dirname(os.path.abspath(__file__))
# print(THIS_PATH)    # d:\Code\ggsddu\source\single_blank
PARENT_PATH = os.path.dirname(THIS_PATH)
# print(PARENT_PATH)  # d:\Code\ggsddu\source
ROOT_PATH = os.path.dirname(PARENT_PATH)
# print(ROOT_PATH)    # d:\Code\ggsddu
sys.path.append(PARENT_PATH)

import math
import sqlite3
import platform

from tkinter import Tk, Entry, Label
from tkinter import IntVar
from tkinter import BOTH
from tkinter.font import Font
from exercise_frame import ExerciseFrame
from misc.constants import Subject

class SingleBlank(ExerciseFrame):
    def __init__(self, master, subject, font_name):
        super().__init__(master, subject, font_name)
        self.init_widgets()

    def init_widgets(self):
        self._promopt_label = Label(self._input_frame, text="请填空:",
            font=self._my_font)
        self._promopt_label.place(x=10, y=7, anchor='nw')
        self._entry_answer = Entry(self._input_frame, font=self._my_bold_font,
            width=67, fg='blue')
        self._entry_answer.place(x=85, y=10, anchor='nw')
        self._entry_answer.focus()
        self._entry_answer.bind("<Return>", self._check)  # 解决回车问题
    
    def _check(self, is_correct=False):
        answer_string = self._entry_answer.get().strip()
        print("user click check and answer=", answer_string)
        is_correct =self.exercise.check(answer_string)

        super()._check(is_correct)


if __name__ == '__main__':
    # 创建主窗口
    root = Tk()
    root.title('Test Single Choice')

    system_name = platform.system()
    # print(system_name)
    if 'Windows' in system_name:
        FONT_NAME = '微软雅黑'
    elif 'Linux' in system_name:
        FONT_NAME = 'Century Schoolbook L'
    else:
        print('Can only support windows and linux')

    width = 1200
    heigh = 600
    screenwidth = root.winfo_screenwidth()
    screenheight = root.winfo_screenheight()
    root.geometry('%dx%d+%d+%d'%(width, heigh, (screenwidth-width)/2, (screenheight-heigh)/2))
    root.resizable(0,0) #防止用户调整尺寸

    my_frame = SingleBlank(root, Subject.MATH, FONT_NAME)

    #进入消息循环
    root.mainloop()
