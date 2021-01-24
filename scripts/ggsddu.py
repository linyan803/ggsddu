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

FONT_NAME = 'Century Schoolbook L'
ENGLISH_SUBJECT = 3 # 英语为3
WORDS_TYPE = 1 # 单词题为1
SCRIPT_PATH = os.path.split(os.path.realpath(sys.argv[0]))[0]

class App:
    def __init__(self, root):
        self.root = root
        
        # 这里先定义所有科目widgets
        self.subject_label_bkg = None
        self.subject_label_yuwen = None
        self.subject_label_shuxue = None
        self.subject_label_yinyu = None

        # 定义单项填空题用到的widgets
        self.single_blank_stem_frame = None
        self.single_blank_canvas_stem = None    # 题干画布
        self.single_blank_text_stem = None      # 题干中的text

        self.single_blank_input_frame = None
        self.single_blank_entry_answer = None   # 输入
        self.single_blank_button_check = None   # 检查答案按钮
        self.single_blank_button_next = None    # 下一步按钮
        self.single_blank_button_return = None  # 返回按钮
        self.single_blank_label_answer = None  

        self.single_blank_counting_frame = None
        self.single_blank_label_times = None
        self.single_blank_label_correct = None
        self.single_blank_label_rate = None
        self.single_blank_lable_weight = None
        self.single_blank_value_times = None
        self.single_blank_value_correct = None
        self.single_blank_value_rate = None
        self.single_blank_value_weight = None

        # 定义英语单词题用到的数据
        self.data_single_blank_exercise_id = -1                    # 试题ID
        self.data_single_blank_stem_string = ''                    # 题干
        self.data_single_blank_is_correct = False                  # 答对没有
        self.data_single_blank_is_lastone = False                  # 还有没有下一题
        self.data_single_blank_answer_string = ''                  # 答案
        self.data_single_blank_answer_variable = StringVar()       # 答案变量
        self.data_single_blank_answer_times = 0                    # 做过几次
        self.data_single_blank_answer_times_variable = StringVar() # 做过几次变量
        self.data_single_blank_correct_times = 0                   # 答对过几次
        self.data_single_blank_correct_variable = StringVar()      # 答对次数变量
        self.data_single_blank_correct_rate_variable = StringVar() # 答对率变量
        self.data_single_blank_weight = 0.0                        # 题目权重
        self.data_single_blank_weight_variable = StringVar()       # 权重变量

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
    
        self.subject_label_bkg = Label(self.root,text='',image=photo_bkg)

        self.subject_label_yuwen = Label(self.root, image=photo_yuwen, cursor="spraycan")
        self.subject_label_yuwen.bind('<Button-1>', self.enter_yuwen)

        self.subject_label_shuxue = Label(self.root, image=photo_shuxue, cursor="spraycan")
        self.subject_label_shuxue.bind('<Button-1>', self.enter_shuxue)
        
        self.subject_label_yinyu = Label(self.root, image=photo_yinyu, cursor="spraycan")
        self.subject_label_yinyu.bind('<Button-1>', self.enter_yinyu)

        self.single_blank_stem_frame = LabelFrame(self.root, text="Vocabulary", 
            font=(FONT_NAME,20,'bold'), padx=5, pady=5, width=820, height=350)
        self.single_blank_canvas_stem = Canvas(self.single_blank_stem_frame)
        self.single_blank_canvas_stem.config(width=780,height=295, relief='solid')

        self.single_blank_input_frame = LabelFrame(self.root, text="Input words", 
            font=(FONT_NAME,20,'bold'), padx=5, pady=5, width=1100, height=150)
        self.single_blank_entry_answer = Entry(self.single_blank_input_frame, 
            font=(FONT_NAME,20,'bold'), width=50)
        self.single_blank_entry_answer.bind("<Return>", self.check_english_words)  # 解决回车问题
        self.single_blank_button_check = Button(self.single_blank_input_frame, text="Check", 
            command=self.check_english_words, font=(FONT_NAME,16,'bold'), width=16)
        self.single_blank_label_answer = Label(self.single_blank_input_frame, textvariable=
            self.data_single_blank_answer_variable,font=(FONT_NAME,20,'bold'))
        self.single_blank_button_next = Button(self.single_blank_input_frame, text="Next", 
            command=self.next_english_words, font=(FONT_NAME,16,'bold'), width=16)
        self.single_blank_button_next.bind("<Return>", self.next_english_words)  # 解决回车问题
        self.single_blank_button_return = Button(self.single_blank_input_frame, text="Return",
            command=self.entry, font=(FONT_NAME,16,'bold'), width=16)
        self.single_blank_button_return.bind("<Return>", self.entry)  # 解决回车问题

        self.single_blank_counting_frame = LabelFrame(self.root, text="Counting", 
            font=(FONT_NAME,20,'bold'), padx=5, pady=5, width=250, height=350)
        self.single_blank_label_times = Label(self.single_blank_counting_frame, text=
            "Times:",font=(FONT_NAME,16), wraplength=80, justify="right")
        self.single_blank_label_correct = Label(self.single_blank_counting_frame, text=
            "Correct:",font=(FONT_NAME,16), wraplength=80, justify="right")
        self.single_blank_lable_rate = Label(self.single_blank_counting_frame, text=
            "Rate:",font=(FONT_NAME,16), wraplength=80, justify="right")
        self.single_blank_lable_weight = Label(self.single_blank_counting_frame, text=
            "Weight:",font=(FONT_NAME,16), wraplength=80, justify="right")
        self.single_blank_value_times = Label(self.single_blank_counting_frame, textvariable=
            self.data_single_blank_answer_times_variable,font=(FONT_NAME,16),
            wraplength=80, justify="left")
        self.single_blank_value_correct = Label(self.single_blank_counting_frame, textvariable=
            self.data_single_blank_correct_variable,font=(FONT_NAME,16),
            wraplength=80, justify="left")
        self.single_blank_value_rate = Label(self.single_blank_counting_frame, textvariable=
            self.data_single_blank_correct_rate_variable,font=(FONT_NAME,16),
            wraplength=80, justify="left")
        self.single_blank_value_weight = Label(self.single_blank_counting_frame, textvariable=
            self.data_single_blank_weight_variable,font=(FONT_NAME,16),
            wraplength=80, justify="left")

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
        base_value = ENGLISH_SUBJECT*10**9 + WORDS_TYPE*10**7
        sql = "select english_words.ID, SUBJECT, TYPE, TIMES, CORRECT, STATUS, WEIGHT, DES, WORD " \
              "from english_words join exercise_info where" \
              "(english_words.ID+%s)==exercise_info.ID order by WEIGHT " \
              "DESC limit 20" % str(base_value)
              
        self.exercises_list = cur.execute(sql).fetchall()
        self.exercises_num = len(self.exercises_list)
        self.current_num = -1  # 切回未开始, 掉next()会+1
        self.next_english_words()


    def check_english_words(self, ev=None):
        user_answer = self.single_blank_entry_answer.get()
        self.data_single_blank_answer_times += 1

        # print(user_answer)
        self.data_single_blank_is_correct = \
            user_answer.strip() == self.data_single_blank_answer_string
        if self.data_single_blank_is_correct:
            correct_string = "Correct"
            self.data_single_blank_correct_times += 1
            self.single_blank_label_answer.configure(fg="green")
        else:
            correct_string = "Wrong"
            self.single_blank_label_answer.configure(fg="red")
        self.data_single_blank_answer_variable.set("%s. The words is: %s" %
            (correct_string, self.data_single_blank_answer_string))
        self.single_blank_label_answer.place(x=5, y=55, anchor='nw')
        if self.data_single_blank_is_lastone:
            # print("show return")
            self.single_blank_button_return.place(x=850, y=55, anchor='nw')
        else:
            # print("show next")
            self.single_blank_button_next.place(x=850, y=55, anchor='nw')
        
        if self.data_single_blank_is_correct:
            if self.data_single_blank_is_lastone: 
                self.single_blank_button_return.focus()
            else:
                self.single_blank_button_next.focus()
        
        new_id = ENGLISH_SUBJECT*10**9 + WORDS_TYPE*10**7 + self.data_single_blank_exercise_id
        new_weight = self.calc_new_weight()
        update_exercise_info_sql = \
            "UPDATE exercise_info SET TIMES=?,CORRECT=?,WEIGHT=? WHERE ID=" + str(new_id)
        data_4_exercise_info_sql = (self.data_single_blank_answer_times,
            self.data_single_blank_correct_times, new_weight)
        cur.execute(update_exercise_info_sql, data_4_exercise_info_sql)
        conn.commit()


    def next_english_words(self, ev=None):
        # english_words.ID, SUBJECT, TYPE, TIMES, CORRECT, STATUS, WEIGHT, DES, WORD
        self.single_blank_button_next.place_forget()
        self.single_blank_button_return.place_forget()
        self.single_blank_label_answer.place_forget()
        self.single_blank_entry_answer.delete(0, 'end')

        self.current_num += 1
        self.data_single_blank_is_lastone = \
            self.current_num == self.exercises_num-1
        # print(self.current_num, self.exercises_num, self.data_single_blank_is_lastone)
        
        exercise = self.exercises_list[self.current_num]
        self.data_single_blank_exercise_id = exercise[0]
        self.data_single_blank_stem_string = exercise[7]
        # 如果有值则删除它
        if self.single_blank_text_stem:
            self.single_blank_canvas_stem.delete(self.single_blank_text_stem)
        self.single_blank_text_stem = \
            self.single_blank_canvas_stem.create_text((0, 0), 
                text=self.data_single_blank_stem_string,
                font=(FONT_NAME,16), anchor='nw', width=760)
        
        self.data_single_blank_answer_string = exercise[8]
        
        # 获取题目的info
        self.data_single_blank_answer_times = exercise[3]
        self.data_single_blank_correct_times = exercise[4]
        self.data_single_blank_weight = exercise[6]
        
        rate_value = self.get_correct_rate()
        rate_value = round(rate_value*100,2)
        answer_times_string    = "%d" % self.data_single_blank_answer_times
        correct_times_string   = "%d" % self.data_single_blank_correct_times
        weight_string          = "%.2f" % self.data_single_blank_weight
        rate_string            = "%.2f%%" % rate_value

        self.data_single_blank_answer_times_variable.set(answer_times_string)
        self.data_single_blank_correct_variable.set(correct_times_string)
        self.data_single_blank_correct_rate_variable.set(rate_string)
        self.data_single_blank_weight_variable.set(weight_string)
        
        self.single_blank_entry_answer.focus()


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
            self.single_blank_stem_frame.place(x=50, y=30, anchor='nw')
            self.single_blank_canvas_stem.place(x=10,y=5)
            self.single_blank_input_frame.place(x=50, y=420, anchor='nw')
            self.single_blank_entry_answer.place(x=5, y=5, anchor='nw')
            self.single_blank_button_check.place(x=850, y=5, anchor='nw')
            self.single_blank_counting_frame.place(x=900, y=30, anchor='nw')
            self.single_blank_label_times.place(x=5, y=5, anchor='nw')
            self.single_blank_value_times.place(x=125, y=5, anchor='nw')
            self.single_blank_label_correct.place(x=5, y=35, anchor='nw')
            self.single_blank_value_correct.place(x=125, y=35, anchor='nw')
            self.single_blank_lable_rate.place(x=5, y=65, anchor='nw')
            self.single_blank_value_rate.place(x=125, y=65, anchor='nw')
            self.single_blank_lable_weight.place(x=5, y=95, anchor='nw')
            self.single_blank_value_weight.place(x=125, y=95, anchor='nw')
        else:
            self.single_blank_stem_frame.place_forget()
            self.single_blank_canvas_stem.place_forget()
            self.single_blank_input_frame.place_forget()
            self.single_blank_entry_answer.place_forget()
            self.single_blank_button_check.place_forget()
            self.single_blank_label_answer.place_forget()
            self.single_blank_button_next.place_forget()
            self.single_blank_button_return.place_forget()
            self.single_blank_counting_frame.place_forget()
            self.single_blank_label_times.place_forget()
            self.single_blank_label_correct.place_forget()
            self.single_blank_lable_rate.place_forget()
            self.single_blank_lable_weight.place_forget()
            self.single_blank_value_times.place_forget()
            self.single_blank_value_correct.place_forget()
            self.single_blank_value_rate.place_forget()
            self.single_blank_value_weight.place_forget()

    def calc_new_weight(self):
        times_weight = 1/2**self.data_single_blank_correct_times
        rate_value = self.get_correct_rate()
        rate_weight = 0.05-math.log((rate_value+0.1)**2, 100)
        print(times_weight, rate_weight)
        return times_weight+rate_weight

    '''
    def fetch_exercise_info(self, subject_id, type_id, id):
        new_id = subject_id*10**9 + type_id*10**7 + id
        sql = "select * from exercise_info where ID=" + str(new_id)
        exercise_infos = cur.execute(sql).fetchall()
        num = len(exercise_infos)
        if 1 != num:
            print("----------Error-------- num = %d ------------" % num)
        
        exercise_info = exercise_infos[0]
        times = exercise_info[3]
        correct_times = exercise_info[4]
        status = exercise_info[5]
        weight = exercise_info[7]
        
        print(times, correct_times, status, weight)
        return (times, correct_times, status, weight)
    '''

    def get_correct_rate(self):
        if 0 == self.data_single_blank_answer_times:
            rate_value = 0.0
        else:
            rate_value = float(self.data_single_blank_correct_times) \
                        /float(self.data_single_blank_answer_times)
        return rate_value


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
    App(root)

    conn = sqlite3.connect(SCRIPT_PATH+"/../database/ggsddu.db")
    cur = conn.cursor()

    #进入消息循环
    root.mainloop()

    cur.close()    
    conn.close()
