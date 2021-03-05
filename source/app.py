#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import sys
import math
import sqlite3
import platform

from tkinter import Tk
from PIL import Image, ImageTk
from tkinter import Frame, Toplevel
from tkinter import Label
from tkinter import X
from tkinter import Canvas
from tkinter import Entry
from tkinter import Button
from tkinter import StringVar

# 常量
from misc.constants import Subject, Model, STYLE, STUDENT
from single_choice.single_choice import SingleChoice
from single_blank.single_blank import SingleBlank
from exercise.exercise import Exercise, ExerciseList

SCRIPT_PATH = os.path.dirname(os.path.abspath(__file__))
print("1. the script path is ", SCRIPT_PATH)  # d:\Code\ggsddu\source

global photo_bkg, photo_chinese, photo_math, photo_english
global photo_physics, photo_biology, photo_geography


class App:
    def __init__(self, the_root):
        print("4. App init now ")
        self.root = the_root
        self.subject_label_bkg = None
        # 所有科目
        self.subject_label_chinese = None
        self.subject_label_math = None
        self.subject_label_english = None
        self.subject_label_physics = None
        self.subject_label_biology = None
        self.subject_label_geography = None
       
        self.exercise_list = None
    
        # 根据题目类型得到题目的框架
        self.model_frame = None       # 不同题型的框架

        #
        self.root.bind("<<check-correct>>", self.check_correct)
        self.root.bind("<<check-wrong>>", self.check_wrong)
        self.root.bind("<<next>>", self.next)
        self.root.bind("<<finish>>",
                       lambda event: self.show_hide_subject_widgets(True))

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
    
        self.subject_label_bkg = Label(
            self.root,
            text='',
            image=photo_bkg)

        self.subject_label_chinese = Label(self.root, image=photo_chinese, cursor="spraycan")
        self.subject_label_chinese.bind(
            '<Button-1>', 
            lambda event: self.enter(subject=Subject.CHINESE))

        self.subject_label_math = Label(self.root, image=photo_math, cursor="spraycan")
        self.subject_label_math.bind(
            '<Button-1>', 
            lambda event: self.enter(subject=Subject.MATH))
        
        self.subject_label_english = Label(self.root, image=photo_english, cursor="spraycan")
        self.subject_label_english.bind(
            '<Button-1>', 
            lambda event: self.enter(subject=Subject.ENGLISH))

        self.subject_label_physics = Label(self.root, image=photo_physics, cursor="spraycan")
        self.subject_label_physics.bind(
            '<Button-1>', 
            lambda event: self.enter(subject=Subject.PHYSICS))

        self.subject_label_biology = Label(self.root, image=photo_biology, cursor="spraycan")
        self.subject_label_biology.bind(
            '<Button-1>', 
            lambda event: self.enter(subject=Subject.BIOLOGY))
        
        self.subject_label_geography = Label(self.root, image=photo_geography, cursor="spraycan")
        self.subject_label_geography.bind(
            '<Button-1>', 
            lambda event: self.enter(Subject.GEOGRAPHY))

    def show_hide_subject_widgets(self, is_show):

        # 显示/隐藏 科目组件
        if is_show:
            if self.model_frame is not None:
                print("app show_hide_subject_widgets Called", is_show)
                self.model_frame.pack_forget()
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
        global subject_conn, subject_cur   # 需要改变

        self.show_hide_subject_widgets(False)
        self.subject = subject
        
        if subject_cur is not None:
            subject_cur.close()
        if subject_conn is not None:
           subject_conn.close()

        subject_db_string = SCRIPT_PATH + "/../database/" + \
                            Subject.get_string(self.subject) + '.db'
        subject_conn = sqlite3.connect(subject_db_string)
        subject_cur = subject_conn.cursor()
        
        if self.exercise_list is not None:
            del self.exercise_list

        self.exercise_list = ExerciseList(
            self.subject,
            personal_conn,
            personal_cur,
            subject_conn,
            subject_cur,
            10)
        self.exercise_list.generate_list()
        self.next(None)
 
    def next(self, event):
        print("app next called")
        if self.model_frame is not None:
            self.model_frame.pack_forget()
            del self.model_frame

        exercise = self.exercise_list.get_next()
        if exercise is None:
            return

        if Model.SINGLE_CHOICE == exercise.model:
            self.model_frame = SingleChoice(self.root, self.subject, FONT_NAME)

        if Model.SINGLE_BLANK == exercise.model: 
            self.model_frame = SingleBlank(self.root, self.subject, FONT_NAME)

        self.model_frame.set_exercise(
            exercise,
            self.exercise_list.seq+1,
            self.exercise_list.num)

    def check_correct(self, event):
        # print("app check_correct called")
        self.exercise_list.write_log(True)
        self.update_personal(self.model_frame.exercise)

    def check_wrong(self, event):
        # print("app check_wrong called")
        self.exercise_list.write_log(False)
        self.update_personal(self.model_frame.exercise)

    def update_personal(self, e):
        # print("app update called")
        self.exercise_list.update(e)


if __name__ == '__main__':
    print("2. Now main start ")
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
    height = 600
    screenwidth = root.winfo_screenwidth()
    screenheight = root.winfo_screenheight()
    root.geometry('%dx%d+%d+%d' %
                  (width, height,
                   (screenwidth-width)/2,
                   (screenheight-height)/2))
    root.resizable(0, 0)  # 防止用户调整尺寸

    # 建立App
    print("3. Create App ")
    app = App(root)

    personal_conn = sqlite3.connect(SCRIPT_PATH+"/../database/LIZHENZHEN.db")
    personal_cur = personal_conn.cursor()
    subject_conn = None
    subject_cur = None

    # 进入消息循环
    root.mainloop()
    
    if subject_cur is not None:
        subject_cur.close()
    if subject_conn is not None:
        subject_conn.close()
    personal_cur.close()    
    personal_conn.close()
