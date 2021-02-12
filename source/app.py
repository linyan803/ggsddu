#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import sys
import math
import sqlite3
import platform

from tkinter import Tk
from PIL import Image, ImageTk
from tkinter import LabelFrame
from tkinter import Label
from tkinter import Canvas
from tkinter import Entry
from tkinter import Button
from tkinter import StringVar
# 常量
from misc.constants import Subject, Model, STEM_TYPE
from single_choice.single_choice import SingleChoice


SCRIPT_PATH = os.path.split(os.path.realpath(sys.argv[0]))[0]

class App:
    def __init__(self, root):
        self.root = root
        self.subject_label_bkg = None
        # 所有科目
        self.subject_label_chinese = None
        self.subject_label_math = None
        self.subject_label_english = None
        self.subject_label_physics = None
        self.subject_label_biology = None
        self.subject_label_geography = None
       
        self.current_subject = ''        # 当前的科目
        self.exercise_list = None
        self.cur_seq = 0                 # 当前题目在list中顺序
    
        # 根据题目类型得到题目的框架
        self.model_frame = None          # 不同题型的框架

        #
        self.init_widgets()
        self.show_hide_subject_widgets(True)

    def init_widgets(self):
                # 进入科目入口
        global photo_bkg, photo_chinese, photo_math, photo_english
        global photo_physics, photo_biology, photo_geography

        image_bkg = Image.open(SCRIPT_PATH+"/../resource/main.png")
        photo_bkg = ImageTk.PhotoImage(image_bkg)
        image_chinese = Image.open(SCRIPT_PATH+"/../resource/yuwen.png")
        photo_chinese= ImageTk.PhotoImage(image_chinese)
        image_math = Image.open(SCRIPT_PATH+"/../resource/shuxue.png")
        photo_math = ImageTk.PhotoImage(image_math)
        image_english = Image.open(SCRIPT_PATH+"/../resource/yinyu.png")
        photo_english = ImageTk.PhotoImage(image_english)
        # new subject
        image_physics = Image.open(SCRIPT_PATH+"/../resource/wuli.png")
        photo_physics = ImageTk.PhotoImage(image_physics)
        image_biology = Image.open(SCRIPT_PATH+"/../resource/shenwu.png")
        photo_biology = ImageTk.PhotoImage(image_biology)
        image_geography = Image.open(SCRIPT_PATH+"/../resource/dili.png")
        photo_geography = ImageTk.PhotoImage(image_geography)
    
        self.subject_label_bkg = Label(self.root,text='',image=photo_bkg)

        self.subject_label_chinese = Label(self.root, image=photo_chinese, cursor="spraycan")
        self.subject_label_chinese.bind(
            '<Button-1>', 
            lambda event:self.enter(subject=Subject.CHINESE))

        self.subject_label_math = Label(self.root, image=photo_math, cursor="spraycan")
        self.subject_label_math.bind(
            '<Button-1>', 
            lambda event:self.enter(subject=Subject.MATH))
        
        self.subject_label_english = Label(self.root, image=photo_english, cursor="spraycan")
        self.subject_label_english.bind(
            '<Button-1>', 
            lambda event:self.enter(subject=Subject.ENGLISH))

        self.subject_label_physics = Label(self.root, image=photo_physics, cursor="spraycan")
        self.subject_label_physics.bind(
            '<Button-1>', 
            lambda event:self.enter(subject=Subject.PHYSICS))

        self.subject_label_biology = Label(self.root, image=photo_biology, cursor="spraycan")
        self.subject_label_biology.bind(
            '<Button-1>', 
            lambda event:self.enter(subject=Subject.BIOLOGY))
        
        self.subject_label_geography = Label(self.root, image=photo_geography, cursor="spraycan")
        self.subject_label_geography.bind(
            '<Button-1>', 
            lambda event:self.enter(Subject.GEOGRAPHY))

    def show_hide_subject_widgets(self, is_show):
        # 显示/隐藏 科目组件
        if is_show:
            self.subject_label_bkg.place(x=0, y=0, anchor='nw')
            self.subject_label_chinese.place(x=50, y=50, anchor='nw')
            self.subject_label_math.place(x=450, y=50, anchor='nw')
            self.subject_label_english.place(x=850, y=50, anchor='nw')
            self.subject_label_physics.place(x=50, y=300, anchor='nw')
            self.subject_label_biology.place(x=450, y=300, anchor='nw')
            self.subject_label_geography.place(x=850, y=300, anchor='nw')
        else:
            self.subject_label_bkg.place_forget()
            self.subject_label_chinese.place_forget()
            self.subject_label_math.place_forget()
            self.subject_label_english.place_forget()
            self.subject_label_physics.place_forget()
            self.subject_label_biology.place_forget()
            self.subject_label_geography.place_forget()

    def enter(self, subject):
        global app
        print("enter subject = %d" % subject)
        self.show_hide_subject_widgets(False)
        self.next()

    def next(self):
        """
        """
        print("app next called")
        self.model_frame = SingleChoice(root, FONT_NAME, self)
        self.model_frame.show()



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

    width = 1200
    heigh = 600
    screenwidth = root.winfo_screenwidth()
    screenheight = root.winfo_screenheight()
    root.geometry('%dx%d+%d+%d'%(width, heigh, (screenwidth-width)/2, (screenheight-heigh)/2))
    root.resizable(0,0) #防止用户调整尺寸

    # 建立App
    app = App(root)

    personal_conn = sqlite3.connect(SCRIPT_PATH+"/../database/PERSONAL.db")
    personal_cur = personal_conn.cursor()
    subject_conn = None
    subject_cur = None

    

    #进入消息循环
    root.mainloop()
    
    if subject_cur is not None:
        subject_cur.close()
    if subject_conn is not None:
        subject_conn.close()
    personal_cur.close()    
    personal_conn.close()
