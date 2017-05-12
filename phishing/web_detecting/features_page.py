#!/usr/bin/env python
# coding:utf-8

import jieba
from sklearn.feature_extraction.text import TfidfTransformer, CountVectorizer


# 将整个文件分成多个part
def get_part(filename):
    with open(filename, 'rb') as f:
        temp = f.readlines()
    # 分割list的算法
    end = temp.index('-'*40+'\r\n')
    part_lst = []
    while end:
        try:
            part_lst.append(temp[0:end])
            start = end + 1
            temp = temp[start:]
            end = temp.index('-'*40+'\r\n')
        except:
            end = False
    # 结束
    return part_lst


# jieba分词
def cut_words(part):
    words = []
    sentence_lst = [sentence.strip() for sentence in part]
    try:
        map(lambda x: words.extend(jieba.lcut(x)), sentence_lst)
        return ' '.join(words)
    except:
        print 'Some part have error in jieba.cut'
        return ' '


# 结合cut_words方法将所有part进行整合以便tfidf算法可以直接接收
def prepare_data(part_lst):
    data = []
    for part in part_lst:
        part_string = cut_words(part)
        data.append(part_string)
    return data


# 用tfidf将对每个part中的所有词进行特征化
def extract_feature(data):
    vector = CountVectorizer()
    transformer = TfidfTransformer()
    tfidf = transformer.fit_transform(vector.fit_transform(data))
    word = vector.get_feature_names()
    weight = tfidf.toarray()
    for i in range(len(weight)):
        print '-----------------output ' + str(i) + 'text---------------------------'
        for j in range(len(word)):
            print word[j], weight[i][j]


if __name__ == '__main__':
    parts_lst = get_part('web_page_features_all.txt')
    data = prepare_data(parts_lst)
    extract_feature(data)
