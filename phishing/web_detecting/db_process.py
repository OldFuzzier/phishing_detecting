#!/usr/bin/python
# -*- coding: utf-8 -*-

from db_config import MyDB


class MyProcess(object):

    def __init__(self):
        super(MyProcess, self).__init__()
        self._db = MyDB()

    def save_sent(self, url, sent):
        sql = 'insert into sent_table (url, sent) values (%s, %s)'
        self._db.my_execute(sql, (url, sent))
        return

    def get_sent(self):
        sql = 'select url, sent from sent_table'
        sents_tuple = self._db.my_select_all(sql)
        return sents_tuple

    def save_word(self, url, word):
        sql = 'insert into word_table (url, word) values (%s, %s)'
        self._db.my_execute(sql, (url, word))
        return

    def get_word(self):
        sql = 'select url, word from word_table'
        words_tuple = self._db.my_select_all(sql)
        return words_tuple

    def save_url(self, url):
        sql = 'insert into url_table (url, flag) values (%s, %s)'
        self._db.my_execute(sql, (url, 1))
        return

    def get_url(self):
        sql = 'select url from url_table'
        url_tuple = self._db.my_select_all(sql)
        return url_tuple





