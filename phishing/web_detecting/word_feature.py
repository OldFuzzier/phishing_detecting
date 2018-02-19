#!/usr/bin/python
# -*- coding: utf-8 -*-
import csv
from collections import defaultdict, OrderedDict

from sklearn.feature_extraction.text import TfidfTransformer, CountVectorizer
from matplotlib import pyplot

from db_process import MyProcess


# 结合cut_words方法将所有part进行整合以便tfidf算法可以直接接收
def prepare_data():
    # data格式为:["word1 word2 word3",
    #             "word4 word5 word6",
    #             "word7 word8 word9"
    #          ]
    mp = MyProcess()
    data = map(lambda tup: tup[1], mp.get_word())
    return data


# 用tfidf将对每个part中的所有词进行特征化
def extract_feature(data):
    vector = CountVectorizer()
    transformer = TfidfTransformer()
    tfidf = transformer.fit_transform(vector.fit_transform(data))
    word = vector.get_feature_names()
    weight = tfidf.toarray()
    for i in range(len(weight)):
        print '-----------------output ' + str(i) + ' text---------------------------'
        for j in range(len(word)):
            if weight[i][j] != 0.0:
                print word[j], weight[i][j]
        break


# 自动打标签
def label_category(lst):
    # 输入为: [[url1, target1], [url2, target1], [url3, target1]
    # [url4, target2], [url5, target3],[url6, target3]]
    # 输出为: [[url1, label1], [url2, label1], [url3, label1]
    # [url1, label4], [url1, label5],[url6, label2]]
    # label 属于 {social, bank, e_business}
    for item_lst in lst:
        s1 = {'Google', 'Facebook', 'Twitter'}
        s2 = {'Google', 'Facebook', 'Twitter'}
        if 1:
            item_lst[1] = 'social'
        elif 2:
            item_lst[1] = 'bank'
        elif 3:
            item_lst[1] = 'e_business'
        else:
            item_lst[1] = 'other'
    return lst


# 获取钓鱼网址
def read_csv(name):
    with open(name) as csvfile:
        reader = csv.reader(csvfile)  # return是个iterable对象
        url_list = [row[-1] for row in reader][1: ]
    return url_list


# 载入文件
def load_file(lst):
    # s 是 set 结构
    with open('brands.txt', 'w+') as f:
        for k, c in lst:
            f.write(k + ' ' + str(c) + '\n')
    return


# 统计每个brand的个数
def count_brand(lst):
    int_dict = defaultdict(int)
    for i in lst:
        if i in int_dict:
            int_dict[i] += 1
        else:
            int_dict[i] = 0
    return int_dict


if __name__ == '__main__':
    lst = read_csv('verified_online.csv')
    d = count_brand(lst)
    x_y_list = OrderedDict(sorted(d.items(), key=lambda x: x[1], reverse=True))
    pyplot.bar(range(len(x_y_list)), x_y_list.values(), tick_label=x_y_list.keys())
    pyplot.show()

    # data = [5, 20, 15, 25, 10]
    # labels = ['Tom', 'Dick', 'Harry', 'Slim', 'Jim']
    # pyplot.bar(range(len(data)), data, tick_label=labels)
    # pyplot.show()

