#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import sys

# 为了引入工程/source目录中的模块
THIS_PATH= os.path.dirname(os.path.abspath(__file__))
# print(THIS_PATH)    # d:\Code\ggsddu\source\input
PARENT_PATH = os.path.dirname(THIS_PATH)
# print(PARENT_PATH)  # d:\Code\ggsddu\source
ROOT_PATH = os.path.dirname(PARENT_PATH)
# print(ROOT_PATH)    # d:\Code\ggsddu
sys.path.append(PARENT_PATH)

import sqlite3
import platform

from tkinter import Tk, Frame, Text, Label, Button, LabelFrame, Canvas, Entry
from tkinter.filedialog import askopenfilename
from tkinter import StringVar
from tkinter import ttk
from tkinter import messagebox
from tkinter.font import Font
from tkinter import BOTH, LEFT, RIGHT, END, NW
from PIL import Image, ImageTk
from shutil import copyfile  # for 文件拷贝

# 常量
from misc.constants import Subject, Model, STYLE, STUDENT
from misc.constants import covert_choice_2_index

class InputWindow(Frame):
    def __init__(self, master, font_name):
        super().__init__(master)                               # 调用父类的初始化函数
        self.master = master
        self.my_font = Font(family=font_name, size=14)
        self.my_small_font = Font(family=font_name, size=12)   # 部分按钮字体小一点
        self.pack(fill=BOTH, expand=1)                         # 自身Frame最大化

        self.pic_stem_file_name = ''                           # 选到的题干图片
        self.pic_ana_file_name = ''                            # 选到的解析图片

        self.db_subject_conn = None
        self.db_subject_cur = None
        self.db_personal_conn = sqlite3.connect(ROOT_PATH+"/database/"+STUDENT+".db")
        self.db_personal_cur = self.db_personal_conn.cursor()

        self.exercise_list = None                              # 查询到的习题列表
        self.exercise_num = -1                                 # 习题列表中的数量
        self.tree_selection = { 'tag': '', 'subject': ''}      # 当前选择的tree元素
        self.selection_var = StringVar()
        self.show = ''                                         # 显示 Stem/Ana

        # 设置ttk的样式
        style = ttk.Style()
        style.theme_use('vista')
        style.configure(
            'Treeview',                                        # treeview的样式
            rowheight=29,               
            font=self.my_font)
        style.configure(             
            'TCombobox')                                       # combobox的样式

        self.command_widgets()
        self.exercise_window()
        self.nav_widgets()                                     # 最后才放nav tree
    
    def __del__(self):
        print("析构函数掉用, 关闭数据库连接")
        if self.db_subject_cur is not None:
            self.db_subject_cur.close()
        if self.db_subject_conn is not None:
            self.db_subject_conn.close()
        if self.db_personal_cur is not None:
            self.db_personal_cur.close()
        if self.db_personal_conn is not None:
            self.db_personal_conn.close()

    def nav_widgets(self):
        self.tree = ttk.Treeview(
            self,
            height=20, 
            show='tree', 
            selectmode='browse')
        english = self.tree.insert('', 0, 'ENGLISH', text='英语', open=True)
        self.tree.insert(english, 0, 'words#ENGLISH', text='单词')
        self.tree.insert(english, 1, 'grammar#ENGLISH', text='语法')
        geography = self.tree.insert('', 0, 'GEOGRAPHY', text='地理', open=True)
        self.tree.insert(geography, 0, '53#GEOGRAPHY', text='5+3')
        self.tree.insert(geography, 1, 'school#GEOGRAPHY', text='校内')
        biology = self.tree.insert('', 0, 'BIOLOGY', text='生物', open=True)
        self.tree.insert(biology, 0, '53#BIOLOGY', text='5+3')
        self.tree.insert(biology, 1, 'school#BIOLOGY', text='校内')
        math = self.tree.insert('', 0, 'MATH', text='数学', open=True)
        self.tree.insert(math, 0, '53#MATH', text='5+3')
        self.tree.insert(math, 1, 'school#MATH', text='校内')
        
        xes_math = self.tree.insert(math,21, 'xes#MATH', text='学而思', open = True)
        self.tree.bind("<<TreeviewSelect>>", self.tree_select)
        self.tree.selection_set(xes_math)  # 缺省选中学而思
        self.tree.place(x=10, y=10, anchor='nw')
    
    def command_widgets(self):
        self.select_label = Label(
            self, 
            textvariable=self.selection_var,
            fg='blue',
            font=self.my_font)
        self.select_label.place(x=225, y=15, anchor='nw')
        self.previous_button = Button(    
            self, 
            text="上一题",
            font=self.my_font, 
            width=8,
            height=1,
            command=self.previous)
        self.previous_button.place(x=450, y=10, anchor='nw')
        self.next_button = Button(
            self, 
            text="下一题",
            font=self.my_font, 
            width=8,
            height=1,
            command=self.next)
        self.next_button.place(x=570, y=10, anchor='nw')
        self.new_button = Button(
            self, 
            text="新建题目",
            font=self.my_font, 
            width=8,
            height=1,
            command=self.new)
        self.new_button.place(x=690, y=10, anchor='nw')
        self.status = StringVar()
        self.status.set('状态:修改->')
        self.notice_label = Label(
            self, 
            textvariable=self.status,
            fg='blue',
            font=self.my_font)
        self.notice_label.place(x=920, y=18, anchor='nw')
        self.submit_button = Button(
            self, 
            text="提交",
            font=self.my_font, 
            width=8,
            height=1,
            command=self.submit)
        self.submit_button.place(x=1030, y=10, anchor='nw')
    
    def exercise_window(self):
        self.exercise_frame = LabelFrame(
            self,
            text="题目", 
            font=self.my_font,
            padx=5,
            pady=5,
            width=970,
            height=534)
        self.exercise_frame.place(x=220, y=60, anchor='nw')
        # ComboBox 字体修改
        self.exercise_frame.option_add("*TCombobox*Listbox*Font",self.my_font)

        # 题型
        self.selected_model = StringVar()
        values = ('单项填空题', '单项选择题') 
        self.model_combobox = ttk.Combobox(
            master=self.exercise_frame,   # 父容器
            height=10,                    # 高度,下拉显示的条目数量
            width=10,                     # 宽度
            state='readonly',             # 设置状态 normal(可选可输入)、readonly(只可选)、 disabled
            cursor='arrow',               # 鼠标移动时样式 arrow, circle, cross, plus...
            font=self.my_font,
            textvariable=self.selected_model,
            values=values)
        self.model_combobox.bind("<<ComboboxSelected>>", self.change_model)
        self.model_combobox.place(x=5, y=5, anchor='nw')   
        self.model_combobox.current(0)    # 设置下拉列表默认显示的值

        # 题干类型
        self.stem_pic_var = StringVar()
        values = ('文字作为题干','图片作为题干') 
        self.stem_combobox = ttk.Combobox(
            master=self.exercise_frame, # 父容器
            height=10, # 高度,下拉显示的条目数量
            width=12, # 宽度
            state='readonly', # 设置状态 normal(可选可输入)、readonly(只可选)、 disabled
            cursor='arrow', # 鼠标移动时样式 arrow, circle, cross, plus...
            font=self.my_font,
            textvariable=self.stem_pic_var,
            values=values)
        self.stem_combobox.bind("<<ComboboxSelected>>", self.show_stem)
        self.stem_combobox.current(0)    # 设置下拉列表默认显示的值
        self.stem_combobox.place(x=155, y=5, anchor='nw')
        self.stem_pic_button = Button(
            self.exercise_frame, 
            text="选择图片",
            font=self.my_small_font, 
            width=8,
            height=1,
            command=self.open_stem_pic)
        self.stem_pic_button.place(x=310, y=2, anchor='nw')

        # 答案
        self.answer_var = StringVar()
        self.answer_label = Label(self.exercise_frame, text='答案:', font=self.my_font)
        self.answer_label.place(x=420, y=5, anchor='nw')   
        self.answer_editor = Entry(
            self.exercise_frame,
            width='20',
            textvariable = self.answer_var,
            font=self.my_font)
        values = ('A', 'B', 'C', 'D') 
        self.answer_combobox = ttk.Combobox(
            master=self.exercise_frame, # 父容器
            height=10, # 高度,下拉显示的条目数量
            width=10, # 宽度
            state='readonly', # 设置状态 normal(可选可输入)、readonly(只可选)、 disabled
            cursor='arrow', # 鼠标移动时样式 arrow, circle, cross, plus...
            font=self.my_font,
            textvariable=self.answer_var,
            values=values)
        self.answer_combobox.current(2)    # 设置下拉列表默认显示的值
        self.change_model(None)           # 调用一次以便按照

        # 解析类型
        self.ana_var = StringVar()
        values = ('文字作为解析', '图片作为解析') 
        self.ana_combobox = ttk.Combobox(
            master=self.exercise_frame, # 父容器
            height=10, # 高度,下拉显示的条目数量
            width=12, # 宽度
            state='readonly', # 设置状态 normal(可选可输入)、readonly(只可选)、 disabled
            cursor='arrow', # 鼠标移动时样式 arrow, circle, cross, plus...
            font=self.my_font,
            textvariable=self.ana_var,
            values=values)
        self.ana_combobox.bind("<<ComboboxSelected>>", self.show_ana)
        self.ana_combobox.current(1)    # 设置下拉列表默认显示的值
        self.ana_combobox.place(x=710, y=5, anchor='nw')
        self.ana_pic_button = Button(
            self.exercise_frame, 
            text="选择图片",
            font=self.my_small_font, 
            width=8,
            height=1,
            command=self.open_ana_pic)
        self.ana_pic_button.place(x=865, y=2, anchor='nw')

        # 题干&解析按钮
        self.stem_button = Button(
            self.exercise_frame,
            text='题干',
            font=self.my_small_font, 
            width=8,
            height=1,
            command=self.show_stem)
        self.stem_button.place(x=5, y=43, anchor='nw')   
        self.ana_button = Button(
            self.exercise_frame,
            text='解析',
            font=self.my_small_font, 
            width=8,
            height=1,
            command=self.show_ana)
        self.ana_button.place(x=95, y=43, anchor='nw') 

        # 题干&解析呈现
        self.stem_editor = Text(
            self.exercise_frame,
            width=86,
            height=16,
            font=self.my_font)
        self.stem_canvas = Canvas(
            self.exercise_frame,
            width=950,
            height=400,
            bg='white')
        self.ana_editor = Text(
            self.exercise_frame,
            width=86,
            height=16,
            font=self.my_font)
        self.ana_canvas = Canvas(
            self.exercise_frame,
            width=950,
            height=400,
            bg='white')

        self.show_stem()           # 调用一次以便按照

    def tree_select(self, event):
        self.selection_var.set(self.tree.selection()[0])
        tags = self.selection_var.get().split('#')
        if len(tags) == 2:
            tag = tags[0]
            subject = tags[1]
        else:
            return 
        
        if tag == self.tree_selection.get('tag') \
           and subject == self.tree_selection.get('subject'):
            # tag 和科目都没有变, 数据不用刷新
            return
        
        if self.db_subject_cur is not None:
            self.db_subject_cur.close()
        if self.db_subject_conn is not None:
            self.db_subject_conn.close()
        
        # 刷新数据
        subject_db_string = ROOT_PATH + "/database/" + subject + '.db'
        self.db_subject_conn = sqlite3.connect(subject_db_string)
        self.db_subject_cur = self.db_subject_conn.cursor()

        if self.exercise_list is not None:
            del self.exercise_list

        # 获取这个科目的题目
        sql_string =                          \
            "SELECT "                         \
                " answer.ID AS id,"           \
                " answer.SUB_ID AS sub_id,"   \
                " answer.MODEL AS model,"     \
                " answer.KEY AS key,"         \
                " answer.E_STYLE AS e_style," \
                " answer.EXPLAIN AS explain," \
                " stem.D_STYLE AS d_style,"   \
                " stem.DES AS stem "          \
            "FROM "                           \
                "answer NATURAL JOIN stem "   \
            "WHERE "                          \
                " NODE='" + self.selection_var.get() + "' " \
            "ORDER BY "                       \
                "ID DESC"
        self.exercise_list = self.db_subject_cur.execute(sql_string).fetchall()
        self.exercise_num = len(self.exercise_list)
        
        # 更换新的select
        self.tree_selection['tag'] = tag
        self.tree_selection['subject'] = subject

        self.seq = -1
        self.next(None)

    def previous(self, event=None):
        pass

    def next(self, event=None):
        global photo_stem, photo_ana
        self.seq += 1
        e = self.exercise_list[self.seq]
        print(e)
        
        model = e[2]
        id = e[0]
        d_style = e[6]
        stem = e[7]
        e_style = e[4]
        explain = e[5]
        key = e[3]

        self.model_combobox.current(model-1)
        model_string = self.model_combobox.get()
        if "单项填空题" == model_string:
            self.answer_var.set(key)
        if "单项选择题" == model_string:
            index = covert_choice_2_index(key)
            self.answer_combobox.current(index)
        self.change_model(None)

        if STYLE.IMG_FILE == d_style and \
            len(stem) > 0:
            self.stem_combobox.current(d_style-1)
            pic_stem_file_name = ROOT_PATH + "/raw/" + \
                self.tree_selection['subject'] + '/' + \
                str(id) + "-stem.png"
            print(pic_stem_file_name)
            image_stem = Image.open(pic_stem_file_name)
            photo_stem = ImageTk.PhotoImage(image_stem)
            self.stem_canvas.delete("all")
            self.stem_canvas.create_image(5,5,anchor=NW,image=photo_stem)
        if STYLE.TEXT_IN_DB == d_style and \
            len(stem) > 0:
            print("stem is ", stem)
            self.stem_combobox.current(d_style-1)
            self.stem_editor.delete('1.0','end')
            self.stem_editor.insert('end',stem)
        
        if STYLE.IMG_FILE == e_style and \
            len(explain) > 0:
            self.ana_combobox.current(e_style-1)
            pic_ana_file_name = ROOT_PATH + "/raw/" + \
                self.tree_selection['subject'] + '/' + \
                str(id) + "-ana.png"
            image_ana = Image.open(pic_ana_file_name)
            photo_ana = ImageTk.PhotoImage(image_ana)
            self.ana_canvas.delete("all")
            self.ana_canvas.create_image(5,5,anchor=NW,image=photo_ana)
        if STYLE.TEXT_IN_DB == e_style and \
            len(explain) > 0:
            self.ana_combobox.current(e_style-1)
            self.ana_editor.delete('1.0','end')
            self.ana_editor.insert('end',stem)
        
        self.show_stem()

    def new(self):
        self.status.set('状态:新建->')

    def submit(self):
        model_string = self.model_combobox.get()
        if "单项选择题" == model_string:
            _model = Model.SINGLE_CHOICE
            _key = self.answer_combobox.get()
        if "单项填空题" == model_string:
            _model = Model.SINGLE_BLANK
            _key = self.answer_editor.get().strip()
        
        stem_type_string = self.stem_combobox.get()
        if "图片作为题干" == stem_type_string:
            _stem_type = STYLE.IMG_FILE
            _des = self.pic_stem_file_name
        if "文字作为题干" == stem_type_string:
            _stem_type = STYLE.TEXT_IN_DB
            _des = self.stem_editor.get(1.0,END).strip()

        print(_des, _key)
        if len(_des) == 0 or len(_key) == 0:
            messagebox.showerror(title = '出错了！',message='题干或者答案不能为空。')
            return
        
        ana_type_string = self.ana_combobox.get()
        if "图片作为解析" == ana_type_string:
            _ana_type = STYLE.IMG_FILE
            _ana = self.pic_ana_file_name
        if "文字作为解析" == ana_type_string:
            _ana_type = STYLE.TEXT_IN_DB
            _ana = self.ana_editor.get(1.0,END).strip()

        values = (_model, _stem_type, _des)
        print("stem: ", values)
        insert_stem_sql = "insert into stem (MODEL, DES_STYLE, DES) values (?,?,?)"
        self.db_subject_cur.execute(insert_stem_sql, values)
        id_query_sql = "select last_insert_rowid() from stem"
        id_query_result = self.db_subject_cur.execute(id_query_sql)
        id_value = id_query_result.fetchone()[0]

        sub_id = 0   # 子题目, 先固定为0
        
        if STYLE.IMG_FILE == _stem_type and len(self.pic_stem_file_name) > 0:
            src_file = os.path.basename(_des)
            name, ext = os.path.splitext(src_file)
            dst_file = ROOT_PATH + '/raw/' + self.tree_selection['subject'] + '/' + \
                str(id_value) + '-stem' + ext
            # print(self.pic_file_name,dst_file)
            copyfile(self.pic_stem_file_name, dst_file)
        if STYLE.IMG_FILE == _ana_type and len(self.pic_ana_file_name) > 0:
            src_file = os.path.basename(_des)
            name, ext = os.path.splitext(src_file)
            dst_file = ROOT_PATH + '/raw/' + self.tree_selection['subject'] + '/' + \
                str(id_value) + '-ana' + ext
            # print(self.pic_file_name,dst_file)
            copyfile(self.pic_ana_file_name, dst_file)

        values = (id_value, sub_id, _model, _key, _ana_type, _ana)
        print("answer: ", values)
        insert_answer_sql = "insert into answer (ID, SUB_ID, ANSWER_TYPE," \
            "KEY, EXPLAIN_TYPE, EXPLAIN) values (?,?,?,?,?,?)"
        self.db_subject_cur.execute(insert_answer_sql, values)

        subject_string = self.tree_selection['subject']
        subject_value = Subject.get_num(subject_string)
        values = (subject_value, id_value, sub_id, 0, 0, 2.0, 0, '')
        print("person: ", values)
        insert_personal_sql = "insert into exercise_info (SUBJECT, ID, " \
            "SUB_ID, TIMES, CORRECT, WEIGHT, STATUS, NOTE) " \
            "values (?,?,?,?,?,?,?,?)"
        self.db_personal_cur.execute(insert_personal_sql, values)

        self.db_subject_conn.commit()
        self.db_personal_conn.commit()

    def open_stem_pic(self):
        global photo_stem
        return_file_name = \
            askopenfilename(
                title='选择题干图片',
                filetypes=[('png file','*.png'),
                           ('jpg file','*.jpg')])
        if len(return_file_name) > 0:
            self.pic_stem_file_name = return_file_name
            image_stem = Image.open(self.pic_stem_file_name)
            photo_stem = ImageTk.PhotoImage(image_stem)
            self.stem_canvas.create_image(5,5,anchor=NW,image=photo_stem)
    
    def open_ana_pic(self):
        global photo_ana
        return_file_name = \
            askopenfilename(
                title='选择题干图片',
                filetypes=[('png file','*.png'),
                           ('jpg file','*.jpg')])
        if len(return_file_name) > 0:
            self.pic_ana_file_name = return_file_name
            # print(self.pic_file_name)
            image_ana = Image.open(self.pic_ana_file_name)
            photo_ana = ImageTk.PhotoImage(image_ana)
            self.ana_canvas.create_image(5,5,anchor=NW,image=photo_ana)
    
    def show_stem(self, event=None):
        print("call show_stem at ", self.show)
        self.show = 'Stem'
        self.ana_button.configure(bg='lightgray', fg='white')
        self.stem_button.configure(bg='blue', fg='white')
        stem_type_string = self.stem_combobox.get()
        print(stem_type_string)

        self.ana_editor.place_forget()
        self.ana_canvas.place_forget()

        if "图片作为题干" == stem_type_string:
            self.stem_editor.place_forget()
            self.stem_canvas.place(x=5, y=80, anchor='nw') 
        if "文字作为题干" == stem_type_string:
            self.stem_canvas.place_forget()
            self.stem_editor.place(x=5, y=80, anchor='nw')
  
    def show_ana(self, event=None):
        print("call show_ana at ", self.show)
        self.show = 'Ana'
        self.stem_button.configure(bg='lightgray', fg='white')
        self.ana_button.configure(bg='blue', fg='white')
        ana_type_string = self.ana_combobox.get()

        self.stem_editor.place_forget()
        self.stem_canvas.place_forget()

        if "图片作为解析" == ana_type_string:
            self.ana_editor.place_forget()
            self.ana_canvas.place(x=5, y=80, anchor='nw') 
        if "文字作为解析" == ana_type_string:
            self.ana_canvas.place_forget()
            self.ana_editor.place(x=5, y=80, anchor='nw')

    def change_model(self, event):
        model_string = self.model_combobox.get()
        # print(model_string)

        if "单项选择题" == model_string:
            self.answer_editor.place_forget()
            self.answer_combobox.place(x=470, y=5, anchor='nw') 
        if "单项填空题" == model_string:
            self.answer_combobox.place_forget()
            self.answer_editor.place(x=470, y=5, anchor='nw') 

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

    width = 1200
    heigh = 600
    screenwidth = root.winfo_screenwidth()
    screenheight = root.winfo_screenheight()
    root.geometry('%dx%d+%d+%d'%(width, heigh, (screenwidth-width)/2, (screenheight-heigh)/2))
    root.resizable(0,0)  # 防止用户调整尺寸

    app = InputWindow(root, FONT_NAME)
    app.mainloop()
