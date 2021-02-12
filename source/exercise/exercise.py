#!/usr/bin/python
# -*- coding: UTF-8 -*-

import math

class Exercise:
    def __init__(self, type, stem, answer_times, answer, 
                 correct_times, weight):
        self.type = type
        self.stem = stem
        self.type_of_stem = self.__get_str_type(self.stem )
        self.answer_times = answer_times
        self.answer = answer
        self.type_of_answer = self.__get_str_type(self.answer)
        self.correct_times = correct_times
        self.weight = weight

    def get_correct_rate(self):
        if 0 == self.answer_times:
            rate_value = 0.0
        else:
            rate_value = float(self.correct_times) \
                        /float(self.answer_times)
        return rate_value
    
    def get_weight(self):
        return self.weight
    
    def check(self, answer):
        pass

    def set_result(self, is_correct):
        pass

    def __calc_new_weight(self):
        """
        重新计算weight
        """
        times_weight = 1/2**self.correct_times
        rate_value = self.get_correct_rate()
        rate_weight = 0.05-math.log((rate_value+0.1)**2, 100)
        print(times_weight, rate_weight)
        return times_weight+rate_weight

    @staticmethod
    def __get_str_type(input_string):
        """
        获取stem/answer的类型, 是文字, 还是图片
        """
        pass