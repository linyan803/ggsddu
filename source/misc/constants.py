#!/usr/bin/python
# -*- coding: UTF-8 -*-

print("5. Constants loaded")


def covert_choice_2_index(char):
    if 'A' == char:
        return 0
    if 'B' == char:
        return 1
    if 'C' == char:
        return 2
    if 'D' == char:
        return 3


class Subject:
    CHINESE = 1
    MATH = 2
    ENGLISH = 3
    PHYSICS = 4
    BIOLOGY = 5
    GEOGRAPHY = 6
    
    @staticmethod
    def get_num(input_string):
        if 'CHINESE' == input_string:
            return Subject.CHINESE
        if 'MATH' == input_string:
            return Subject.MATH 
        if 'ENGLISH' == input_string:
            return Subject.ENGLISH      
        if 'PHYSICS' == input_string:
            return Subject.PHYSICS
        if 'BIOLOGY' == input_string:
            return Subject.BIOLOGY
        if 'GEOGRAPHY' == input_string:
            return Subject.GEOGRAPHY

    @staticmethod
    def get_string(input_value):
        if Subject.CHINESE == input_value:
            return 'CHINESE'
        if Subject.MATH == input_value:
            return 'MATH'
        if Subject.ENGLISH == input_value:
            return 'ENGLISH'   
        if Subject.PHYSICS == input_value:
            return 'PHYSICS'
        if Subject.BIOLOGY == input_value:
            return 'BIOLOGY'
        if Subject.GEOGRAPHY == input_value:
            return 'GEOGRAPHY'


class Model:
    SINGLE_BLANK = 1
    SINGLE_CHOICE = 2
    MULTI_BLANK = 3
    MULTI_CHOICE = 4


class STYLE:
    TEXT_IN_DB = 1
    IMG_FILE = 2
    MD_IN_DB = 3
    NOTHING = 255
