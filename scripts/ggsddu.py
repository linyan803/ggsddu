#!/usr/bin/python
# -*- coding: UTF-8 -*-

from tkinter import Tk
from PIL import Image, ImageTk
from tkinter import Label

# 初始化Tk()
the_window = Tk()

# 全局的初始按钮
image_bkg = Image.open("D:\\code\\english_words\\main2.png")
photo_bkg = ImageTk.PhotoImage(image_bkg)

image_yuwen = Image.open("D:\\code\\english_words\\yuwen.png")
photo_yuwen = ImageTk.PhotoImage(image_yuwen)
image_shuxue = Image.open("D:\\code\\english_words\\shuxue.png")
photo_shuxue = ImageTk.PhotoImage(image_shuxue)
image_yinyu = Image.open("D:\\code\\english_words\\yinyu.png")
photo_yinyu = ImageTk.PhotoImage(image_yinyu)

# 全局科目按钮列表
subject_list = []

def init_windows():
    global the_window
    #设置标题
    the_window.title('The notebook of wrong questions for Li Zhenzhen')
    the_window.state("zoomed")
    the_window.resizable(width=False, height=False)


def put_init_image():
    global the_window
    global photo_bkg, photo_yuwen, photo_shuxue, photo_yinyu
 
    image_label = Label(the_window,text='The notebook of wrong questions @ Li Zhenzhen',font=('MV BOLI',30),image=photo_bkg)
    image_label.place(x=0, y=0, anchor='nw')

    label_yuwen = Label(the_window, image=photo_yuwen, cursor="spraycan")
    subject_list.append(label_yuwen)
    label_yuwen.bind('<Button-1>', enter_yuwen)
    label_yuwen.place(x=150, y=300, anchor='nw')

    label_shuxue = Label(the_window, image=photo_shuxue, cursor="spraycan")
    subject_list.append(label_shuxue)
    label_shuxue.bind('<Button-1>', enter_shuxue)
    label_shuxue.place(x=600, y=300, anchor='nw')
    
    label_yinyu = Label(the_window, image=photo_yinyu, cursor="spraycan")
    subject_list.append(label_yinyu)
    label_yinyu.bind('<Button-1>', enter_yinyu)
    label_yinyu.place(x=1050, y=300, anchor='nw')

def enter_yuwen(event):
    clear_frame()


def enter_shuxue(event):
    clear_frame()


def enter_yinyu(event):
    clear_frame()


def clear_frame():
    global subject_list
    for i in range(len(subject_list)):
        button = subject_list[i]
        button.place_forget() 


def show_beidanci():
    pass


if __name__ == '__main__':
    put_init_image()
    init_windows()

    #进入消息循环
    the_window.mainloop()
