#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
该模块用于所有分类器训练预测等
'''

import numpy as np

from sklearn.model_selection import train_test_split  # 训练测试数据相互分离
from sklearn.model_selection import cross_val_score  # 交叉验证
from sklearn.metrics import recall_score  # 召回率
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import BernoulliNB, MultinomialNB
from sklearn.externals import joblib  # 用于存储和导入模型

from db.db_process import MyProcess


# 计时器
def timer(func):
    def wrapper(*args, **kwargs):
        import time
        start = time.time()
        func(*args, **kwargs)
        end = time.time()
        print 'Cost %f seconds' % (end - start) + '\n'
        return
    return wrapper


class MyClassier(MyProcess):

    def __init__(self):
        super(MyClassier, self).__init__()
        self.clf_dict = {'BernoulliNB':BernoulliNB, 'MultinomialNB':MultinomialNB,
                         'SVC':SVC, 'KNeighborsClassifier':KNeighborsClassifier}

    # 从数据库中获取需要训练的数据
    def load_train_data(self, flag):
        # params flag: 什么类型的训练数据
        # return dataset: array格式的数据 [[0,0,0,1,0,1], [0,0,0,1,0,-1], ....]
        print '--------We are loading data--------------'
        # 判断是导入什么类型的训练数据
        if flag == 'url':
            # url数据使用过file获取的
            arr_lst = []  # 每个每个特征转化为array个时候都要添加到这个list中
            with open('url_detecting/url_data/features2.txt', 'rb') as f:
                url_list = f.readlines()
            for url_string in url_list:
                if len(url_string) > 1:  # 除去空的字符串
                    arr_lst.append(np.array(eval(url_string.strip())))
                else:
                    continue
            dataset = np.array(arr_lst)
        elif flag == 'text':
            # text数据是通过数据库获取的
            feature_list = self.get_feature()  # 从数据库取出feature组成的序列
            arr_lst = map(lambda feature_tuple: np.array(eval(feature_tuple[0])), feature_list)
            dataset = np.array(arr_lst)  # 转换成分类器可以作为输入的格式
        else:
            raise Exception
        print 'finish load \n'
        return dataset

    # 训练和测试，普通的验证
    @timer
    def train_test(self, name, dataset):
        # params name: 分类器名字
        # params dataset: array格式的数据 [[0,0,0,1,0,1], [0,0,0,1,0,-1], ....]
        # return clf的对象(训练后)
        print '---------We are training By %s------------' % name
        data = dataset[:, :-1]
        target = dataset[:, -1]
        clf_obj = self.clf_dict[name]()  # 生成分类器对象
        x_train, x_test, y_train, y_test = train_test_split(data, target, test_size=0.2)  # 分离train和test
        clf_obj.fit(x_train, y_train)  # 训练
        predict = clf_obj.predict(x_test)  # 预测
        right = sum(predict == y_test)  # 预测结果比对
        recall = recall_score(y_test, predict, average='macro')  # 找回率
        print name + ': '
        print '正确率: %f%%\t' % (right*100.0/predict.shape[0]) + '召回率: %f%%\t' % (recall*100) +\
              '训练数据: %d\t' % x_train.shape[0] + '测试数据: %d' % x_test.shape[0]
        return clf_obj

    # 训练和测试，利用交叉验证
    @timer
    def cross_train_test(self, name, dataset):
        # params name: 分类器名字
        # params dataset: array格式的数据 [[0,0,0,1,0,1], [0,0,0,1,0,-1], ....]
        print '---------We are training By %s------------' % name
        clf_obj = self.clf_dict[name]()  # 生成分类器对象
        data = dataset[:, :-1]
        target = dataset[:, -1]
        scores = cross_val_score(clf_obj, data, target, cv=3)  # 交叉验证, cv=3是处理3词交叉验证
        print ' 交叉验证正确率: %f%%\t' % (scores.mean()*100)
        return

    # 用于存入训练模型
    def save_model(self, clf, name):
        # params clf: 分类器
        # params name: 模型名称
        joblib.dump(clf, 'model/%s.m'%name)
        return

    # 用于获取模型
    def get_model(self, name):
        # params name: 模型名称
        classifier = joblib.load('model/%s.m'%name)
        return classifier

    # 分类器训练和保存模型的主函数
    def main_train_test(self, flag, clf_name, file_name):
        dataset = self.load_train_data(flag)
        clf_obj = self.train_test(clf_name, dataset)
        # self.cross_train_test(clf_name, dataset)
        # self.save_model(clf_obj, file_name)
        return



# def main_train_test():
#     clfs = {'多项式朴素贝叶斯': MultinomialNB, '支持向量机分类器': SVC, 'K邻近分类器': KNeighborsClassifier}
#     dataset = load_data()
#     data = dataset[:, :1165]  # 因为有1165个特征
#     target = dataset[:, 1165]
#     x_train, x_test, y_train, y_test = train_test_split(data, target, test_size=0.2)
#     for clf_name, clf in clfs.items():
#         clfter(clf_name, clf, x_train, y_train, x_test, y_test, data, target)
#     return


# def test_KNN():
#     dataset = load_data()
#     data = dataset[:, :1165]
#     target = dataset[:, 1165]
#     x_train, x_test, y_train, y_test = train_test_split(data, target, test_size=0.1)
#     clf = KNeighborsClassifier(algorithm='kd_tree')
#     clf.fit(x_train, y_train)
#     return clf


if __name__ == '__main__':
    obj = MyClassier().main_train_test('url', 'SVC', 'hahah')
    obj = MyClassier().main_train_test('url', 'KNeighborsClassifier', 'haha')
    obj = MyClassier().main_train_test('url', 'MultinomialNB', 'hahah')