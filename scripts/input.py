#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import sys
import math
import sqlite3
import platform

from tkinter import Tk, Frame, Text, Label, Button, LabelFrame, StringVar
from tkinter import ttk
from tkinter.font import Font
from tkinter import BOTH, LEFT, RIGHT, END


class InputWindow(Frame):
    def __init__(self, master, font_name):
        Frame.__init__(self, master)
        self.master = master
        self.my_font = Font(family=font_name, size=16)
        self.my_title_font = Font(family=font_name, size=32, weight='bold')
        self.pack(fill=BOTH, expand=1)    
        self.nav_widgets()
        self.command_widgets()
    
    def nav_widgets(self):
        self.title = Label(
            self.master, 
            text="试题输入",
            font=self.my_title_font)
        self.title.place(x=10, y=10, anchor='nw')
        self.tree = ttk.Treeview(self.master, height=20)
        style = ttk.Style()
        style.configure("Treeview.Heading", font=self.my_font)
        self.tree.insert('', 0, 'english', text='英语')      # english =
        self.tree.insert('', 0, 'geography', text='地理')    # geography =
        self.tree.insert('', 0, 'biology', text='生物')      # biology = 
        self.tree.place(x=10, y=50, anchor='nw')
    
    def command_widgets(self):
        self.previous_button = Button(    
            self.master, 
            text="<-",
            font=self.my_font, 
            width=4,
            height=1,
            command=self.previous)
        self.previous_button.place(x=320, y=10, anchor='nw')
        self.next_button = Button(
            self.master, 
            text="->",
            font=self.my_font, 
            width=4,
            height=1,
            command=self.next)
        self.next_button.place(x=400, y=10, anchor='nw')
        self.new_button = Button(
            self.master, 
            text="+",
            font=self.my_font, 
            width=4,
            height=1,
            command=self.new)
        self.new_button.place(x=470, y=10, anchor='nw')
        self.status = StringVar()
        self.status.set('修改')
        self.notice_label = Label(
            self.master, 
            textvariable=self.status,
            font=self.my_font)
        self.notice_label.place(x=540, y=10, anchor='nw')
        self.submit_button = Button(
            self.master, 
            text="提交",
            font=self.my_font, 
            width=4,
            height=1,
            command=self.new)
        self.submit_button.place(x=610, y=10, anchor='nw')
    
    def exercise_window(self):
        self.exercise_frame = LabelFrame()
        self.model_label = Label()
        self.model_combobox = ttk.Combobox()
        self.answer_label = Label()
        self.answer_editor = Text(
            self,
            width='1',
            font=self.my_font)
        self.stem_label = Label()
        self.stem_editor = Text()

    def previous(self):
        pass

    def next(self):
        pass

    def new(self):
        self.status.set('新建')

    def submit(self):
        pass


if __name__ == '__main__':
    # 创建主窗口
    root = Tk()
    root.geometry("1024x640")
    root.title('Input Exercise')

    system_name = platform.system()
    # print(system_name)
    if 'Windows' in system_name:
        FONT_NAME = '微软雅黑'
    elif 'Linux' in system_name:
        FONT_NAME = 'Century Schoolbook L'
    else:
        print('Can only support windows and linux')

    app = InputWindow(root, FONT_NAME)
    app.mainloop()