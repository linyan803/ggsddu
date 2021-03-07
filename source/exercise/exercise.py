#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import sys

# 为了引入工程/source目录中的模块
THIS_PATH= os.path.dirname(os.path.abspath(__file__))
# print(THIS_PATH)    # d:\Code\ggsddu\source\exercise
PARENT_PATH = os.path.dirname(THIS_PATH)
# print(PARENT_PATH)  # d:\Code\ggsddu\source
ROOT_PATH = os.path.dirname(PARENT_PATH)
# print(ROOT_PATH)    # d:\Code\ggsddu
sys.path.append(PARENT_PATH)

import time
import math
import sqlite3

from misc.constants import Model, Subject

class Exercise:
    def __init__(self, id, sub_id, answer_times, correct_times, weight,
                 model, key, d_style, stem, e_style, explain):
        self.id = id
        self.sub_id = sub_id
        self.answer_times = answer_times
        self.correct_times = correct_times    
        self.weight = weight
        self.model = model
        self.key = key
        self.d_style = d_style
        self.stem = stem
        self.e_style = e_style
        self.explain = explain

    def get_correct_rate(self):
        if 0 == self.answer_times:
            rate_value = 0.0
        else:
            rate_value = float(self.correct_times) \
                        /float(self.answer_times)
        return rate_value
    
    def check(self, answer):
        if Model.SINGLE_BLANK == self.model or \
           Model.SINGLE_CHOICE == self.model:
            is_correct = (answer == self.key.strip())
        if is_correct:
            self.correct_times += 1
 
        self.answer_times += 1
        self.__calc_new_weight()

        return is_correct

    def __calc_new_weight(self):
        """
        重新计算weight
        """
        times_weight = 1/2**self.correct_times
        rate_value = self.get_correct_rate()
        rate_weight = 0.05-math.log((rate_value+0.1)**2, 100)
        print(times_weight, rate_weight)
        self.weight = times_weight+rate_weight


class ExerciseList:
    def __init__(self, subject, p_conn, p_cur, s_conn, s_cur, num=20):
        self.subject = subject
        # 数据库操作全在在ExerciseList
        self.p_conn = p_conn
        self.p_cur = p_cur
        self.s_conn = s_conn
        self.s_cur = s_cur
        self.num = num
        self.list = []

    def get_subject(self):
        return self.subject

    def get_next(self):
        self.seq += 1
        if self.seq < self.num:
            node_in_list = self.list[self.seq]
        else:
            return None
    
        id = node_in_list[0]
        sub_id = node_in_list[1]
        answer_times = node_in_list[2]
        correct_times = node_in_list[3]
        weight = node_in_list[4]

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
            "WHERE id=%d and sub_id=%d" % (id, sub_id)
                
        list_of_result = self.s_cur.execute(sql_string).fetchall()
        num = len(list_of_result)
        print("练习题 id=%d, sub_id=%d 有%d个" % (id, sub_id, num))

        e = list_of_result[0]

        # id, sub_id, answer_times, correct_times, weight,
        # model, key, d-style, stem, e-style, explain
        exercise = Exercise( 
            e[0],  # id
            e[1],  # sub_id
            answer_times,
            correct_times,
            weight,
            e[2], # model
            e[3], # key
            e[6], # d_style
            e[7], # stem
            e[4], # e_style
            e[5]  # explain
        )
        return exercise

    def generate_list(self):
        # 获取这个科目的题目
        sql_string = "select ID, SUB_ID, TIMES, CORRECT, WEIGHT, STATUS, " \
            "NOTE from exercise_info where SUBJECT=" + str(self.subject) + \
            " order by WEIGHT DESC,ID DESC limit 10;"

        self.list = self.p_cur.execute(sql_string).fetchall()
        self.num = len(self.list)
        print("get %d for the %s" % (self.num, Subject.get_string(self.subject)))
        self.seq = -1  # 切回未开始, 掉next()会+1

    def write_log(self, is_correct):
        print("write log for ", is_correct)
        if self.seq < self.num:
            node_in_list = self.list[self.seq]
        else:
            return None

        id = node_in_list[0]
        sub_id = node_in_list[1]
        time_string = time.strftime('%Y-%m-%d %H:%M:%S',
                                    time.localtime(time.time()))
        
        values = (time_string, id, sub_id, str(is_correct))
        print("update log values is ", values)
        sql_string = "INSERT INTO logs (TIME_STAMP, ID, SUB_ID, CORRECT) " \
                     "VALUES(?,?,?,?)"
        self.p_cur.execute(sql_string, values)
        self.p_conn.commit()

    def update(self, e):
        """
        将一条exercise的信息重新存储到数据库中
        """
        # 
        sql_string = "UPDATE exercise_info SET TIMES=?, CORRECT=?, WEIGHT=?" \
                     " WHERE SUBJECT=? AND ID=? AND SUB_ID=?;"
        values = (
            e.answer_times,
            e.correct_times,
            e.weight,  
            self.subject,  
            e.id,
            e.sub_id
        )
        print("update exercise_info values is", values)
        self.p_cur.execute(sql_string, values)
        self.p_conn.commit()


if __name__ == '__main__':
    # 测试代码
    personal_conn = sqlite3.connect(ROOT_PATH+"/database/LIZHENZHEN.db")
    personal_cur = personal_conn.cursor()
    
    subject_db_string = ROOT_PATH + "/database/" + \
                        Subject.get_string(Subject.MATH) + '.db'
    subject_conn = sqlite3.connect(subject_db_string)
    subject_cur = subject_conn.cursor()

    exercise_list = ExerciseList(
        Subject.MATH,
        personal_cur,
        subject_cur
    )
    exercise_list.generate_list()

    # 第一个exercise, 求答对率
    e = exercise_list.get_next()
    print("success rate is ", e.get_correct_rate())
    # 第二个exercise, check下
    e = exercise_list.get_next()
    print(e.check('D'))
    print('No %d exercise weight is %f' % (e.id, e.weight))
    # 第三个, 检查是否是None
    e = exercise_list.get_next()
    print(e)

    if subject_cur is not None:
        subject_cur.close()
    if subject_conn is not None:
        subject_conn.close()
    personal_cur.close()    
    personal_conn.close()