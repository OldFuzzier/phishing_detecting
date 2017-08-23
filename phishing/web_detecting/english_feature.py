#!/usr/bin/env python
# coding:utf-8

import nltk
from nltk.corpus import stopwords

from db_process import MyProcess


def segment_word(sent):
    english_punctuations = [',', '.', ':', ';', '?', '(', ')', '[', ']', '&', '!', '*', '@', '#', '$', '%', '\'']
    words = nltk.word_tokenize(sent)
    filter_words = filter(lambda x: x not in english_punctuations and x not in stopwords.words('english'), words)
    return filter_words


def data_prepare():
    mp = MyProcess()
    sents_phishing = mp.get_sent()
    for sents_tuple in sents_phishing:
        words_lst = []  # 全部sent总体的list
        url = sents_tuple[0]
        sents_string = sents_tuple[1]
        class_ = sents_tuple[2]
        sents_lst = sents_string.split('   ')  # 从数据库取出的是tuple形式
        for sent in sents_lst:
            words = segment_word(sent)
            word_string = ' '.join(words)  # 一个sent中的words
            words_lst.append(word_string)
        mp.save_word(url, ' '.join(words_lst), class_)
    return


if __name__ == '__main__':
    pass


