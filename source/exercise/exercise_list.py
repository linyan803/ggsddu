#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
一次练习的列表
"""

class ExerciseList:
    def __init__(self, subject, personal_cur, subject_cur, num=20):
        self.subject = subject
        self.p_cur = personal_cur
        self.p_cur = subject_cur
        self.num = num
        self.exercise_list = []
        self.count = 0

    def get_subject(self):
        """
        获取科目
        """
        return self.subject

    def get_next(self):
        """
        """
        if self.count < self.num:
            exercise = self.exercise_list[self.count]
        else:
            exercise = None
        return exercise

    def generate_list(self):
        """
        """
        base_value = 2
        sql = "select english_words.ID, SUBJECT, TYPE, TIMES, CORRECT, STATUS, WEIGHT, DES, WORD " \
              "from english_words join exercise_info where" \
              "(english_words.ID+%s)==exercise_info.ID order by WEIGHT DESC, english_words.ID " \
              "DESC limit 20" % str(base_value)
        self.exercises_list = self.p_cur.execute(sql).fetchall()
        self.num = len(self.exercises_list)

    def update(self, exercise):
        """
        将一条exercise的信息重新存储到数据库中
        """
        pass