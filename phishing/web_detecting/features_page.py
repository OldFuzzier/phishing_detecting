#!/usr/bin/env python
# coding:utf-8

import itertools

import jieba
from sklearn.feature_extraction.text import TfidfTransformer, CountVectorizer


def get_cut_words(filename):
    word = []
    with open(filename, 'rb') as f:
        temp = f.readlines()
    sentence = [words.strip() for words in temp]
    map(lambda x: word.extend(jieba.lcut(x)), sentence)
    return ' '.join(word)


def manage_word(*word_lst):
    lst = []
    for i in word_lst:
        lst.append(i)
    return lst


def extract_feature(lst):
    vector = CountVectorizer()
    transformer = TfidfTransformer()
    tfidf = transformer.fit_transform(vector.fit_transform(lst))
    word = vector.get_feature_names()
    weight = tfidf.toarray()
    for i in range(len(weight)):
        print '-----------------output ' + str(i) + 'text---------------------------'
        for j in range(len(word)):
            print word[j], weight[i][j]


if __name__ == '__main__':
    word1 = get_cut_words('web_page_features.txt')
    word2 = get_cut_words('web_page_features2.txt')
    lst = manage_word(word1, word2)
    extract_feature(lst)



