#!/usr/bin/python
# -*- coding: utf-8 -*-

from db_config import MyDB


class MyProcess(object):

    def __init__(self):
        self._db = MyDB()

    def save_sent(self, site, sent, class_):
        sql = 'insert into sent_table (site, sent, class) values (%s, %s, %s)'
        self._db.my_execute(sql, (site, sent, class_))
        return

    def get_sent(self):
        sql = 'select site, sent, class from sent_table'
        sents_tuple = self._db.my_select_all(sql)
        return sents_tuple

    def save_word(self, site, word, class_):
        sql = 'insert into word_table (site, word, class) values (%s, %s, %s)'
        self._db.my_execute(sql, (word,))
        return

    def get_word(self):
        sql = 'select site, sent, class from word_table'
        words_tuple = self._db.my_select_all(sql)
        return words_tuple

mp = MyProcess()
print mp.get_sent()


