#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import sys
import math
import sqlite3
import platform

from tkinter import Tk, Frame, LabelFrame, Canvas, Label, Radiobutton, Button
from tkinter import IntVar
from tkinter import BOTH
from tkinter.font import Font


class SingleChoice(Frame):
    def __init__(self, master, font_name, app):
        super().__init__(master)
        self.root = master
        self.my_font = Font(family=font_name, size=16)
        self.my_bold_font = Font(family=font_name, size=16, weight='bold')
        self.my_big_font = Font(family=font_name, size=32, weight='bold')
        self.choice_list = IntVar()
        self.init_window()
        self.app=app
    
    def init_window(self):
        self.pack(fill=BOTH, expand=1)
        # 题干显示窗口
        self.single_choice_stem_frame = LabelFrame(
            self,
            text="题目描述", 
            font=self.my_font, 
            padx=5, 
            pady=5, width=900, height=500)
        self.single_choice_canvas_stem = Canvas(self.single_choice_stem_frame)
        self.single_choice_canvas_stem.config(width=880,height=460, relief='solid')
        # 选项框
        self.single_choose_frame = LabelFrame(
            self,
            text="请选择", 
            font=self.my_font, 
            padx=5, 
            pady=5, width=260, height=500)
        self.choice_A = Radiobutton(
            self.single_choose_frame,
            variable=self.choice_list,
            value=1,
            font=self.my_bold_font, 
            text='A')
        self.choice_B = Radiobutton(
            self.single_choose_frame,
            variable=self.choice_list,
            font=self.my_bold_font, 
            value=2,
            text='B')
        self.choice_C = Radiobutton(
            self.single_choose_frame,
            variable=self.choice_list,
            font=self.my_bold_font, 
            value=3,
            text='C')
        self.choice_D = Radiobutton(
            self.single_choose_frame,
            variable=self.choice_list,
            font=self.my_bold_font, 
            value=4,
            text='D')
        # 执行按钮
        self.button_check = Button(
            self.single_choose_frame, 
            text="对了错了？",
            font=self.my_font, 
            width=16,
            height=2,
            command=self.check)
        self.button_check.bind("<Return>", self.check)  # 解决回车问题
        # 执行按钮
        self.button_next = Button(
            self.single_choose_frame, 
            text="下一道题",
            font=self.my_font, 
            width=16,
            height=2,
            command=self.next)
        self.button_check.bind("<Return>", self.next)  # 解决回车问题

    def show(self):
            self.single_choice_stem_frame.place(x=10, y=10, anchor='nw')
            self.single_choice_canvas_stem.place(x=0, y=0, anchor='nw')
            self.single_choose_frame.place(x=920, y=10, anchor='nw')
            self.choice_A.place(x=10, y=30, anchor='nw')
            self.choice_B.place(x=10, y=80, anchor='nw')
            self.choice_C.place(x=10, y=130, anchor='nw')
            self.choice_D.place(x=10, y=180, anchor='nw')
            self.button_check.place(x=10, y=300, anchor='nw')
            self.button_next.place(x=10, y=380, anchor='nw')

    def hide(self):
            self.single_choice_stem_frame.place_forget()
            self.single_choice_canvas_stem.place_forget()
            self.single_choose_frame.place_forget()
            self.choice_A.place_forget()
            self.choice_B.place_forget()
            self.choice_C.place_forget()
            self.choice_D.place_forget()
            self.button_check.place_forget()
            self.button_next.place_forget()

    def check(self):
        pass

    def next(self):
         self.app.next()


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

    my_frame = SingleChoice(root, FONT_NAME)
    my_frame.show()

    #进入消息循环
    root.mainloop()
