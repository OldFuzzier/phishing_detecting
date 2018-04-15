#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
用于phishing_detecting项目中所有数据库之间的处理
'''


from db_config import MyDB


class MyProcess(object):

    def __init__(self):
        super(MyProcess, self).__init__()
        self._db = MyDB()

    def save_phish_sent(self, url, html, sent, cate):
        sql = 'insert into phish_sent_table (url, html_text, string_sent, cate) values (%s, %s, %s, %s)'
        self._db.my_execute(sql, (url, html, sent, cate))
        return

    def get_phish_sent(self):
        sql = 'select url, string_sent, cate from phish_sent_table'
        sents_tuple = self._db.my_select_all(sql)
        return sents_tuple

    def save_normal_sent(self, url, html, sent, cate):
        sql = 'insert into normal_sent_table (url, html_text, string_sent, cate) values (%s, %s, %s, %s)'
        self._db.my_execute(sql, (url, html, sent, cate))
        return

    def get_normal_sent(self):
        sql = 'select url, string_sent, cate from normal_sent_table'
        sents_tuple = self._db.my_select_all(sql)
        return sents_tuple

    def save_alexa_url(self, url, cate):
        sql = 'insert into alexa_url_table (url, cate) values (%s, %s)'
        self._db.my_execute(sql, (url, cate))
        return

    def get_alexa_url(self):
        sql = 'select url, cate from alexa_url_table'
        url_tuple = self._db.my_select_all(sql)
        return url_tuple

    def save_normal_url(self, url, cate):
        sql = 'insert into normal_url_table (url, cate) values (%s, %s)'
        self._db.my_execute(sql, (url, cate))
        return

    def get_normal_url(self):
        sql = 'select url, cate from normal_url_table'
        url_tuple = self._db.my_select_all(sql)
        return url_tuple

    def save_phish_word(self, url, word, cate):
        sql = 'insert into phish_word_table (url, word, cate) values (%s, %s, %s)'
        self._db.my_execute(sql, (url, word, cate))
        return

    def get_phish_word(self):
        sql = 'select url, word, cate from phish_word_table'
        words_tuple = self._db.my_select_all(sql)
        return words_tuple

    def save_normal_word(self, url, word, cate):
        sql = 'insert into normal_word_table (url, word, cate) values (%s, %s, %s)'
        self._db.my_execute(sql, (url, word, cate))
        return

    def get_normal_word(self):
        sql = 'select url, word, cate from normal_word_table'
        words_tuple = self._db.my_select_all(sql)
        return words_tuple

    def save_word(self, url, word):
        sql = 'insert into word_table (url, word) values (%s, %s)'
        self._db.my_execute(sql, (url, word))
        return

    def get_word(self):
        sql = 'select url, word from word_table'
        words_tuple = self._db.my_select_all(sql)
        return words_tuple

    def save_feature(self, feature, is_phish):
        sql = 'insert into train_table (feature, is_phish) values (%s, %s)'
        self._db.my_execute(sql, (feature, is_phish))
        return

    def get_feature(self):
        sql = 'select feature from train_table'
        feature_tuple = self._db.my_select_all(sql)
        return feature_tuple

    def delete_blank_word(self, flag):
        # 用于清理word_table中空白word
        # flag : phish or normal
        if flag == 'phish':
            sql = 'delete from phish_word_table where length(word)<1'
        else:
            sql = 'delete from normal_word_table where length(word)<1'
        self._db.my_execute(sql)
        return


if __name__ == '__main__':
    pass



