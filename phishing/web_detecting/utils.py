#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
该模块主要是web_detecting的辅助方法
'''

import csv
from collections import defaultdict

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
        url_list = [(row[1], row[-1]) for row in reader][501: ]  # 读取结构为[(url1, cate1), (url2, cate2), ...]
    return url_list


# 载入文件
def load_file(lst, filename):
    # s 是 set 结构
    with open(filename, 'w+') as f:
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


# 整理成需要的数据
def format_data(dct):
    label_all = sorted(dct.items(), key=lambda x: x[1], reverse=True)
    # label_filter = filter(lambda s: s[1]>10, table_all[1:])  # 踢出了other
    return label_all