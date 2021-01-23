#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os
import sys
import sqlite3
# import platform
from tkinter import Tk
from PIL import Image, ImageTk
from tkinter import Label
from tkinter import Canvas
from tkinter import Entry
from tkinter import Button
from tkinter import StringVar

FONT_NAME = 'Century Schoolbook L'

SCRIPT_PATH = os.path.split(os.path.realpath(sys.argv[0]))[0]

class App:
    def __init__(self, frame):
        self.frame = frame
        
        # 这里先定义所有科目widgets
        self.subject_label_bkg = None
        self.subject_label_yuwen = None
        self.subject_label_shuxue = None
        self.subject_label_yinyu = None

        # 定义单项填空题用到的widgets
        self.single_blank_label_type = None     # 类型
        self.single_blank_canvas_stem = None    # 题干画布
        self.single_blank_text_stem = None      # 题干中的text
        self.single_blank_label_input = None    
        self.single_blank_entry_answer = None   # 输入框
        self.single_blank_button_check = None   # 检查答案按钮
        self.single_blank_button_next = None    # 下一步按钮
        self.single_blank_button_return = None  # 返回按钮
        self.single_blank_label_answer = None  

        # 定义英语单词题用到的数据
        self.data_single_blank_stem_string = ''                    # 题干
        self.data_single_blank_is_correct = False                  # 答对没有
        self.data_single_blank_is_lastone = False                  # 还有没有下一题
        self.data_single_blank_answer_string = ''                  # 答案
        self.data_single_blank_answer_variable = StringVar()       # 答案变量
        self.data_single_blank_answer_times = 0                    # 做过几次
        self.data_single_blank_answer_times_variable = StringVar() # 做过几次变量
        self.data_single_blank_correct_times = 0                   # 答对过几次
        self.data_single_blank_correct_variable = StringVar()      # 答对次数变量
        self.data_single_blank_correct_rate = 0.0                  # 答对率
        self.data_single_blank_correct_rate_variable = StringVar() # 答对率变量

        # 题目数据
        self.exercises_num = 0
        self.current_num = -1     # -1 代表未开始
        self.exercises_list = []

        self.init_widgets()
        self.entry()

    def init_widgets(self):
                # 进入科目入口
        global photo_bkg, photo_yuwen, photo_shuxue, photo_yinyu

        image_bkg = Image.open(SCRIPT_PATH+"/../resource/main.png")
        photo_bkg = ImageTk.PhotoImage(image_bkg)
        image_yuwen = Image.open(SCRIPT_PATH+"/../resource/yuwen.png")
        photo_yuwen = ImageTk.PhotoImage(image_yuwen)
        image_shuxue = Image.open(SCRIPT_PATH+"/../resource/shuxue.png")
        photo_shuxue = ImageTk.PhotoImage(image_shuxue)
        image_yinyu = Image.open(SCRIPT_PATH+"/../resource/yinyu.png")
        photo_yinyu = ImageTk.PhotoImage(image_yinyu)
    
        self.subject_label_bkg = Label(self.frame,text='',image=photo_bkg)

        self.subject_label_yuwen = Label(self.frame, image=photo_yuwen, cursor="spraycan")
        self.subject_label_yuwen.bind('<Button-1>', self.enter_yuwen)

        self.subject_label_shuxue = Label(self.frame, image=photo_shuxue, cursor="spraycan")
        self.subject_label_shuxue.bind('<Button-1>', self.enter_shuxue)
        
        self.subject_label_yinyu = Label(self.frame, image=photo_yinyu, cursor="spraycan")
        self.subject_label_yinyu.bind('<Button-1>', self.enter_yinyu)
    
        self.single_blank_label_type = Label(self.frame,text='Vocabulary:',font=(FONT_NAME,20,'bold'))
        
        self.single_blank_canvas_stem = Canvas(self.frame)
        self.single_blank_canvas_stem.config(width=1000,height=400, relief='solid')

        self.single_blank_label_input = Label(self.frame,text='Input words:',font=(FONT_NAME,20,'bold'))

        self.single_blank_entry_answer = Entry(self.frame, font=(FONT_NAME,16,'bold'), width=35)

        self.single_blank_button_check = Button(self.frame, text="Check", command=self.check_answer,
            font=(FONT_NAME,20,'bold'), width=11, height=1)

        self.single_blank_label_answer = Label(self.frame, textvariable=
            self.data_single_blank_answer_variable,font=(FONT_NAME,20,'bold'))
                
        self.single_blank_button_next = Button(self.frame, text="Next", command=self.next,
            font=(FONT_NAME,20,'bold'), width=11, height=1)

        self.single_blank_button_return = Button(self.frame, text="Return", command=self.entry,
            font=(FONT_NAME,20,'bold'), width=11, height=1)


    def entry(self):
        self.show_hide_single_blank_widgets(False)
        self.show_hide_subject_widgets(True)


    def enter_yuwen(self, event):
        pass


    def enter_shuxue(self, event):
        pass


    def enter_yinyu(self, event):
        self.show_hide_subject_widgets(False)
        self.show_hide_single_blank_widgets(True)
        sql = "select * from english_words"
        self.exercises_list = cur.execute(sql).fetchall()
        self.exercises_num = len(self.exercises_list)
        self.current_num = -1  # 切回未开始, 掉next()会+1
        self.next()


    def check_answer(self):
        user_answer = self.single_blank_entry_answer.get()
        # print(user_answer)
        self.data_single_blank_is_correct = \
            user_answer.strip() == self.data_single_blank_answer_string

        if self.data_single_blank_is_correct:
            correct_string = "Correct"
            self.single_blank_label_answer.configure(fg="green")
        else:
            correct_string = "Wrong"
            self.single_blank_label_answer.configure(fg="red")
        self.data_single_blank_answer_variable.set("%s. The words is: %s" %
            (correct_string, self.data_single_blank_answer_string))
        self.single_blank_label_answer.place(x=100, y=480, anchor='nw')
        if self.data_single_blank_is_lastone:
            # print("show return")
            self.single_blank_button_return.place(x=500, y=480, anchor='nw')
        else:
            # print("show next")
            self.single_blank_button_next.place(x=800, y=480, anchor='nw')


    def next(self):
        self.single_blank_button_next.place_forget()
        self.single_blank_button_return.place_forget()
        self.single_blank_label_answer.place_forget()
        self.single_blank_entry_answer.delete(0, 'end')

        self.current_num += 1
        self.data_single_blank_is_lastone = \
            self.current_num == self.exercises_num-1
        # print(self.current_num, self.exercises_num, self.data_single_blank_is_lastone)
        exercise = self.exercises_list[self.current_num]
        
        self.data_single_blank_stem_string = exercise[1]
        # 如果有值则删除它
        if self.single_blank_text_stem:
            self.single_blank_canvas_stem.delete(self.single_blank_text_stem)
        self.single_blank_text_stem = \
            self.single_blank_canvas_stem.create_text((10, 10), 
            text=self.data_single_blank_stem_string,
            font=(FONT_NAME,16), anchor='nw', width=1000)
        self.data_single_blank_answer_string = exercise[2]


    def show_hide_subject_widgets(self, is_show):
        # 显示/隐藏 科目组件
        if is_show:
            self.subject_label_bkg.place(x=0, y=0, anchor='nw')
            self.subject_label_yuwen.place(x=50, y=150, anchor='nw')
            self.subject_label_shuxue.place(x=450, y=150, anchor='nw')
            self.subject_label_yinyu.place(x=850, y=150, anchor='nw')
        else:
            self.subject_label_bkg.place_forget()
            self.subject_label_yuwen.place_forget()
            self.subject_label_shuxue.place_forget()
            self.subject_label_yinyu.place_forget()


    def show_hide_single_blank_widgets(self, is_show):
        # 显示/隐藏 单项填空组件
        if is_show:
            self.single_blank_label_type.place(x=100, y=50, anchor='nw')
            # 如果有值则删除它
            if self.single_blank_text_stem:
                self.single_blank_canvas_stem.delete(self.single_blank_text_stem)
            self.single_blank_text_stem = \
                self.single_blank_canvas_stem.create_text((10, 10), 
                    text=self.data_single_blank_stem_string,
                    font=(FONT_NAME,16), anchor='nw', width=1000)
            self.single_blank_canvas_stem.place(x=100,y=100)
            self.single_blank_label_input.place(x=100, y=420, anchor='nw')
            self.single_blank_entry_answer.place(x=300, y=422, anchor='nw')
            self.single_blank_entry_answer.focus ()
            self.single_blank_button_check.place(x=800, y=415, anchor='nw')
            # 点击check_button才能显示
            # self.single_blank_label_answer.place(x=100, y=580, anchor='nw')
            # self.single_blank_button_next.place(x=1100, y=580, anchor='nw')
        else:
            self.single_blank_label_type.place_forget()
            self.single_blank_canvas_stem.place_forget()
            self.single_blank_label_input.place_forget()
            self.single_blank_entry_answer.place_forget()
            self.single_blank_button_check.place_forget()
            self.single_blank_label_answer.place_forget()
            self.single_blank_button_next.place_forget()
            self.single_blank_button_return.place_forget()


if __name__ == '__main__':
    # 创建主窗口
    root = Tk()
    root.title('The notebook of wrong questions for Li Zhenzhen')
    '''
    if(platform.system()=='Windows'):
        the_window.state("normal")
        the_window.resizable(width=False, height=False)
    elif(platform.system()=='Linux'):
        w = the_window.winfo_screenwidth()
        h = the_window.winfo_screenheight()
        the_window.geometry("%dx%d" %(w, h))
    else:
        print('Can only support windows and linux')
    '''
    width = 1200
    heigh = 600
    screenwidth = root.winfo_screenwidth()
    screenheight = root.winfo_screenheight()
    root.geometry('%dx%d+%d+%d'%(width, heigh, (screenwidth-width)/2, (screenheight-heigh)/2))
    root.resizable(0,0) #防止用户调整尺寸

    # 建立App
    App(root)

    conn = sqlite3.connect(SCRIPT_PATH+"/../database/ggsddu.db")
    cur = conn.cursor()

    #进入消息循环
    root.mainloop()

    cur.close()    
    conn.close()
