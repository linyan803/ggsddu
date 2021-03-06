#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
GGSDDU 的启动程序
1. git 主目录
2. 获取当前登录用户名，当前登录用户名即数据库文件名
   检查数据库文件如果不存在，那么创建数据库文件
3. 读取history.list中最后一行的日期, 没有即为0
   将PERSONAL.db中晚于上面日期的条目插入到新建数据库中
"""

import os
import datetime
import sqlite3
import platform
import time

from tkinter import Tk, Text
from tkinter import RIGHT, Y, END, ALL
from tkinter.font import Font
from shutil import copyfile  # for 文件拷贝

from misc.log import Log

SCRIPT_PATH = os.path.dirname(os.path.abspath(__file__))
MAX_LINES = 14  # 界面仅能显示12行
WAIT_TIME = 1000


class StartWindow:
    def __init__(self, the_root, font_name):
        self.log = Log()
        self.root = the_root
        self.my_font = Font(family=font_name, size=12)
        self.db_file = None
        self.show_text = Text(
            self.root,
            bg='darkgray',  # darkslategray
            fg='black',
            font=self.my_font,
            relief='ridge',
            spacing1=3,
            spacing2=3,
            spacing3=3
        )
        self.show_text.pack(side="left", fill="both", expand=True)
        self.step_count = 0
        self.lines = []
        self._insert_line("正在初始化GGSDDU，请稍后")
        self._new_exercise_list = []
        self.is_exception = False

        self.show_text.after(WAIT_TIME, self._auto_step)

    def _insert_line(self, line):
        if len(line) > 0:
            self.log.info(line)
        else:
            return

        if MAX_LINES == len(self.lines):
            del self.lines[0]
        self.lines.append(line)

        all_text = ''
        for line in self.lines:
            all_text += ' ' + line + '\n'

        self.show_text.delete(1.0, END)
        self.show_text.insert(1.0, all_text[:-1])

    def _git_ggsddu(self):
        # 1. git 主目录
        command_string = "cd " + SCRIPT_PATH+"\\.. &" \
                         "cd &" \
                         "git pull\n"
        res = os.popen(command_string)
        info_list = res.read().splitlines()
        for line in info_list:
            # print("show %s to text" % line)
            self._insert_line(line)

    def _check_personal_database(self):
        # 2. 获取当前登录用户名，当前登录用户名即数据库文件名
        #    检查数据库文件如果不存在，那么创建数据库文件
        user_name = os.getlogin()
        self.db_file = SCRIPT_PATH + '/../database/' + user_name + '.db'
        if os.path.exists(self.db_file):
            self._insert_line("个人数据库(%s)已存在" % self.db_file)
        else:
            self._insert_line("创建个人数据库(%s)" % self.db_file)
            copyfile(
                src=SCRIPT_PATH + '/../database/PERSONAL.db',
                dst=self.db_file
            )

    def _check_history_file(self, history_file):
        is_exist = os.path.exists(history_file)
        self._insert_line("历史文件%s存在？%s" % (history_file, str(is_exist)))
        if not is_exist:
            with open(history_file, 'w') as f:
                self._insert_line("新建历史文件，写入20201210102234")
                f.write("20201210102234\n")

    def _get_new_exercise_list(self):
        # 读取history.list中最后一行的日期, 没有即为0
        # 将PERSONAL.db中晚于上面日期的条目插入到新建数据库中
        history_file = SCRIPT_PATH + '/history.list'
        self._check_history_file(history_file)
        with open(history_file, 'r') as f:
            all_history = f.readlines()
            last_line = all_history[len(all_history)-1]
            last_line = last_line.strip()
            self._insert_line("获取上次更新时间为%s" % last_line)

        last_update_time = datetime.datetime.strptime(
            last_line.split("\n")[0],
            "%Y%m%d%H%M%S"
        )
        last_update_time_string =\
            datetime.datetime.strftime(
                last_update_time,
                '%Y.%m.%d %H:%M:%S')
        db_file = SCRIPT_PATH + '/../database/PERSONAL.db'
        personal_conn = sqlite3.connect(db_file)
        personal_cur = personal_conn.cursor()
        sql_string = "select * from exercise_info where TIME_STAMP > ?"
        self._new_exercise_list = personal_cur.execute(
            sql_string,
            (last_update_time_string,)).fetchall()
        num = len(self._new_exercise_list)
        self._insert_line("获取更新的题目%d个" % num)
        personal_cur.close()
        personal_conn.close()

        return num

    @staticmethod
    def _tuple_2_string(input_tuple):
        return_string = ''
        for item in input_tuple:
            return_string += str(item) + ', '
        return return_string[:-1]

    def _insert_new_exercises(self):
        # print("_insert_new_exercises num=", len(self._new_exercise_list))
        personal_conn = sqlite3.connect(self.db_file)
        personal_cur = personal_conn.cursor()
        insert_sql_string = "insert into exercise_info " \
                            "(SUBJECT, ID, SUB_ID, TIMES, CORRECT, " \
                            "WEIGHT, STATUS, NOTE, TIME_STAMP) "\
                            "values (?,?,?,?,?,?,?,?,?)"
        query_sql_string = "select * from exercise_info " \
                           "where SUBJECT=? and ID=? and SUB_ID=?"

        for exercise in self._new_exercise_list:
            # 先查这个exercise是否存在
            subject = exercise[0]
            id = exercise[1]
            sub_id = exercise[2]
            all_query = personal_cur.execute(
                query_sql_string,
                (subject, id, sub_id)).fetchall()
            if 1 == len(all_query):  # 已存在
                self._insert_line(
                    self._tuple_2_string(all_query[0]) + " 已存在")
                continue

            self._insert_line(
                " 插入新题目  " + self._tuple_2_string(exercise))
            personal_cur.execute(
                insert_sql_string,
                exercise)

        personal_conn.commit()
        personal_cur.close()
        personal_conn.close()

    def _auto_step(self):
        self.step_count += 1
        if 1 == self.step_count:
            self._insert_line("1. 检查和更新程序")
            self._git_ggsddu()
            self.show_text.after(WAIT_TIME, self._auto_step)
        if 2 == self.step_count:
            self._insert_line("2. 检查个人数据库是否存在")
            self._check_personal_database()
            self.show_text.after(WAIT_TIME, self._auto_step)
        if 3 == self.step_count:
            self._insert_line("3. 检查数据库更新")
            num = self._get_new_exercise_list()
            if 0 == num:
                self.step_count += 1  # 跳过下一步
            self.show_text.after(WAIT_TIME, self._auto_step)
        if 4 == self.step_count:
            self._insert_line("4. 更新题目")
            self._insert_new_exercises()
            self.show_text.after(WAIT_TIME, self._auto_step)
        if 5 == self.step_count:
            if self.is_exception:
                print("出错了")
            else:
                history_file = SCRIPT_PATH + '/history.list'
                with open(history_file, 'a') as f:
                    now_string = time.strftime(
                        '%Y%m%d%H%M%S',
                        time.localtime(time.time()))
                    f.write(now_string+'\n')
                root.destroy()


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

    width = 600
    height = 385
    screenwidth = root.winfo_screenwidth()
    screenheight = root.winfo_screenheight()
    root.geometry('%dx%d+%d+%d' %
                  (width, height,
                   (screenwidth-width)/2,
                   (screenheight-height)/2))
    root.overrideredirect(True)
    # 建立App
    app = StartWindow(root, FONT_NAME)

    # personal_conn = sqlite3.connect(SCRIPT_PATH+"/../database/LIZHENZHEN.db")
    # personal_cur = personal_conn.cursor()

    # 进入消息循环
    root.mainloop()
    print("start frame quit")
    command = 'python ' + SCRIPT_PATH + '/app.py'
    os.system(command)
