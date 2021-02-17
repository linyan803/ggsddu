#!/usr/bin/python
# -*- coding: UTF-8 -*-

'''
试题呈现类的基类
'''
import os
import platform

from tkinter import Tk, Frame, LabelFrame, Canvas, Label, Radiobutton, Button
from tkinter import IntVar, StringVar
from tkinter import BOTH, NW
from tkinter.font import Font
from misc.constants import Subject, Model, STYLE
from PIL import Image, ImageTk

SCRIPT_PATH= os.path.dirname(os.path.abspath(__file__))
# print(SCRIPT_PATH) # d:\Code\ggsddu\source

ANSWER_PSEUDO = '李蓁蓁, 加油！'

class ExerciseFrame(Frame):
    def __init__(self, master, subject, font_name):
        super().__init__(master)
        self.master = master
        self.subject = subject
        self.pack(fill=BOTH, expand=1)                         # 自身Frame最大化

        # counting 显示信息
        # self._answer_times = 0                    # 做过几次
        self._answer_times_variable = StringVar()   # 做过几次变量
        # self._correct_times = 0                   # 答对过几次
        self._correct_variable = StringVar()        # 答对次数变量
        self._rate_variable = StringVar()           # 答对率变量
        # self._weight = 0.0                        # 题目权重
        self._weight_variable = StringVar()         # 权重变量  
        self._info_variable = StringVar()

        # self._answer_string = ''                  # 答案
        self._answer_variable = StringVar()         # 答案变量
        self._answer_variable.set(ANSWER_PSEUDO)

        # 字体
        self._my_font = Font(family=font_name, size=14)
        self._my_small_font = Font(family=font_name, size=12)
        self._my_bold_font = Font(family=font_name, size=14, weight='bold')
        self._my_big_font = Font(family=font_name, size=28, weight='bold')

        self._init_stem()
        self._init_counting()
        self._init_input()

    def _init_stem(self):
        # 题干&解析按钮
        self._stem_button = Button(
            self,
            text='题干',
            font=self._my_small_font, 
            width=8,
            height=1,
            relief='flat',
            command=self._show_stem)
        self._stem_button.place(x=15, y=5, anchor='nw')   
        self._ana_button = Button(
            self,
            text='解析',
            font=self._my_small_font, 
            width=8,
            height=1,
            relief='flat',
            command=self._show_ana)
        # self._ana_button.place(x=100, y=5, anchor='nw')

        self._canvas_stem = Canvas(self)
        self._canvas_stem.config(
            width=900,
            height=400, 
            bg='white',
            relief='flat')
        self._canvas_ana = Canvas(self)
        self._canvas_ana.config(
            width=900,
            height=400, 
            bg='white',
            relief='flat')
        self._show_stem()

    def _init_counting(self):
        self._counting_frame = LabelFrame(self, text="统计", 
            font=self._my_bold_font, padx=5, pady=5, width=250, height=416)
        
        self._label_times = Label(self._counting_frame, text="答题次数:",
            font=self._my_font, width=8, anchor="e")
        self._label_correct = Label(self._counting_frame, text="答对次数:",
            font=self._my_font, width=8, anchor="e")
        self._lable_rate = Label(self._counting_frame, text="答 对  率:",
            font=self._my_font, width=8, anchor="e")
        self._lable_weight = Label(self._counting_frame, text="权      值:",
            font=self._my_font, width=8, anchor="e")

        self._value_times = Label(self._counting_frame, textvariable=
            self._answer_times_variable,font=self._my_font, wraplength=80, justify="left")
        self._value_correct = Label(self._counting_frame, textvariable=
            self._correct_variable,font=self._my_font, wraplength=80, justify="left")
        self._value_rate = Label(self._counting_frame, textvariable=
            self._rate_variable,font=self._my_font, wraplength=80, justify="left")
        self._value_weight = Label(self._counting_frame, textvariable=
            self._weight_variable,font=self._my_font, wraplength=80, justify="left")

        self._label_info = Label(self._counting_frame, textvariable=self._info_variable,
            font=self._my_big_font, wraplength=180, justify="right", fg='blue')

        self._counting_frame.place(x=935, y=30, anchor='nw')
        self._label_times.place(x=5, y=5, anchor='nw')
        self._value_times.place(x=125, y=5, anchor='nw')
        self._label_correct.place(x=5, y=35, anchor='nw')
        self._value_correct.place(x=125, y=35, anchor='nw')
        self._lable_rate.place(x=5, y=65, anchor='nw')
        self._value_rate.place(x=125, y=65, anchor='nw')
        self._lable_weight.place(x=5, y=95, anchor='nw')
        self._value_weight.place(x=125, y=95, anchor='nw')

        self._label_info.place(x=70, y=300, anchor='nw')

    def _init_input(self):
        self._input_frame = LabelFrame(self, text="答题区域", 
            font=self._my_bold_font, padx=5, pady=5, width=1170, height=138)
        self._input_frame.place(x=15, y=450, anchor='nw')

        self._button_check = Button(self._input_frame, text="提交答案", 
            command=self._check, font=self._my_font, width=16)
        self._button_check.place(x=930, y=2, anchor='nw')
        self._label_answer = Label(self._input_frame, textvariable=
            self._answer_variable,font=self._my_font, fg='black')
        self._label_answer.place(x=10, y=55, anchor='nw')

        self._button_next = Button(self._input_frame, text="下一道题", 
            command=self._next, font=self._my_font, width=16)
        self._button_next.bind("<Return>", self._next)  # 解决回车问题

        self._button_return = Button(self._input_frame, text="回主界面",
            command=self._return, font=self._my_font, width=16)
        self._button_return.bind("<Return>", self._return)  # 解决回车问题

    def set_exercise(self, e, seq, total):
        global photo_stem, photo_ana

        self.exercise = e
        self.seq = seq
        self.total = total
        
        string_info = "%d/%d" % (self.seq, self.total)
        self._info_variable.set(string_info)

        self._answer_times_variable.set(self.exercise.answer_times)
        self._correct_variable.set(self.exercise.correct_times)
        rate_value = round(self.exercise.get_correct_rate()*100, 2)
        self._rate_variable.set(str(rate_value)+'%')
        self._weight_variable.set(round(self.exercise.weight, 2))
        
        if STYLE.IMG_FILE == self.exercise.d_style and \
            len(self.exercise.stem) > 0:
            pic_stem_file_name = SCRIPT_PATH + "/../raw/" + \
                Subject.get_string(self.subject) + '/' + \
                str(self.exercise.id) + "-stem.png"
            image_stem = Image.open(pic_stem_file_name)
            photo_stem = ImageTk.PhotoImage(image_stem)
            self._canvas_stem.create_image(5,5,anchor=NW,image=photo_stem)

        if STYLE.TEXT_IN_DB == self.exercise.d_style and \
            len(self.exercise.stem) > 0:
            self._canvas_stem.create_text((10, 5), 
                text=self.exercise.stem,
                font=self._my_font, anchor='nw', width=860)

        if STYLE.IMG_FILE == self.exercise.e_style and \
            len(self.exercise.explain) > 0:
            pic_ana_file_name = SCRIPT_PATH + "/../raw/" + \
                Subject.get_string(self.subject) + '/' + \
                str(self.exercise.id) + "-ana.png"
            image_ana = Image.open(pic_ana_file_name)
            photo_ana = ImageTk.PhotoImage(image_ana)
            self._canvas_ana.create_image(5,5,anchor=NW,image=photo_ana)
        
        if STYLE.TEXT_IN_DB == self.exercise.e_style and \
            len(self.exercise.explain) > 0:
            self._canvas_ana.create_text((10, 5), 
                text=self.exercise.explain,
                font=self._my_font, anchor='nw', width=860)

    def _check(self, is_correct=False):
        print("ExerciseFrame _check, is_correct=", is_correct)
        self._answer_times_variable.set(self.exercise.answer_times)
        self._correct_variable.set(self.exercise.correct_times)
        rate_value = round(self.exercise.get_correct_rate()*100, 2)
        self._rate_variable.set(str(rate_value)+'%')
        self._weight_variable.set(round(self.exercise.weight, 2))

        if is_correct:
            self.master.event_generate("<<check-correct>>")
        else:            
            self.master.event_generate("<<check-wrong>>")

        promopt_string = ''
        # check之后显示答案和ana按钮
        if is_correct:
            self._label_answer.configure( fg='green')
            promopt_string += "答对了! "
            if self.seq == self.total:
                self._button_return.place(x=930, y=50, anchor='nw')
                self._button_return.focus()
            else:
                self._button_next.place(x=930, y=50, anchor='nw')
                self._button_next.focus()
        else:
            self._label_answer.configure( fg='red')
            promopt_string += "答错了! 正确答案是: " + self.exercise.key + "。"
        
        if len(self.exercise.explain) > 0:
            promopt_string += " 请点击解析按钮查看解析。"
            self._ana_button.place(x=100, y=5, anchor='nw')
        
        self._answer_variable.set(promopt_string)

    def _next(self, event=None):
        print("Exercise Frame _next called")
        self.master.event_generate("<<next>>")

    def _return(self, event=None):
        self.master.event_generate("<<finish>>")

    def _show_stem(self):
        self._ana_button.configure(bg='lightgray', fg='black')
        self._stem_button.configure(bg='blue', fg='white')
        self._canvas_ana.place_forget()
        self._canvas_stem.place(x=14, y=42, anchor='nw')

    def _show_ana(self):
        self._stem_button.configure(bg='lightgray', fg='black')
        self._ana_button.configure(bg='blue', fg='white')
        self._canvas_stem.place_forget()
        self._canvas_ana.place(x=14, y=42, anchor='nw')


if __name__ == '__main__':
    # 创建主窗口
    root = Tk()
    root.title('Test exercise')

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

    my_frame = ExerciseFrame(root, Subject.MATH, FONT_NAME)

    #进入消息循环
    root.mainloop()