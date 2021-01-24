#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os
import sys
import sqlite3
import xlrd

script_path = os.path.split(os.path.realpath(sys.argv[0]))[0]
conn = sqlite3.connect(script_path+"/ggsddu.db")
ccur = conn.cursor()


SUBJECT_VALUE = 3 # 英语为3
TYPE_VALUE = 1 # 单词题为1
ENGLISG_WORDS_FILE = script_path+"/../raw/english/english_words.xls"


def handle_english_words():
    workbook = xlrd.open_workbook(ENGLISG_WORDS_FILE)
    sheet = workbook.sheet_by_index(0)
    for i in range(1,sheet.nrows):
        id = sheet.cell(i,0).value
        des = sheet.cell(i,1).value
        word = sheet.cell(i,2).value
        note = sheet.cell(i,3).value
        
        is_update = "update" in note
        is_exist =  query_english_words(id)

        if is_update and is_exist:
            update_english_words(id, des, word, note)
        elif not is_exist:
            new_english_words(id, des, word, note)
        else:
            print("%d,%s,%s,%s already exist"%(id, des, word, note))


def update_english_words(id, des, word, note):
    update_new_english_word_sql = \
        "UPDATE english_words SET DES=?,WORD=?,NOTE=? WHERE ID=%d" % id
    data_4_english_word_sql = (des,word,note)
    cur.execute(update_new_english_word_sql,data_4_english_word_sql)
    conn.commit()


def new_english_words(id, des, word, note):
    insert_new_english_word_sql = \
        "INSERT INTO english_words(ID,DES,WORD,NOTE)  VALUES(?,?,?,?)"
    data_4_english_word_sql = (id,des,word,note)
    cur.execute(insert_new_english_word_sql,data_4_english_word_sql)

    new_id = SUBJECT_VALUE*10**9 + TYPE_VALUE*10**7 + id
    insert_new_exercise_info_sql = \
        "INSERT INTO exercise_info(ID,SUBJECT,TYPE,TIMES,CORRECT,STATUS,NOTE,WEIGHT) " \
        "VALUES(?,'english','words',0,0,0,'',0)"
    cur.execute(insert_new_exercise_info_sql,(new_id,))
    
    conn.commit()


def query_english_words(id):
    """
    查询是否id已经在数据库中有值了
    """
    sql = "select * from english_words where ID=?"
    values = cur.execute(sql,(id,)).fetchall()
    num = len(values)
    if num > 0:
        return True
    else:
        return False


if __name__ == '__main__':
    conn = sqlite3.connect(script_path+"/ggsddu.db")
    cur = conn.cursor()
    
    handle_english_words()

    cur.close()    
    conn.close()
