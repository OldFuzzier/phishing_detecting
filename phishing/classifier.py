#!/usr/bin/env python
# coding:utf-8

import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline


nbc_1 = Pipeline([
    ('clf', MultinomialNB())
])
nbc_2 = Pipeline([
    ('clf', SVC(kernel='rbf'))
])
nbc_3 = Pipeline([
    ('clf', KNeighborsClassifier())
])
# classier
nbcs = [nbc_1, nbc_2, nbc_3]


def timer(func):
    def wrapper(*args, **kwargs):
        import time
        start = time.time()
        func(*args, **kwargs)
        end = time.time()
        print 'Cost %f seconds' % (end - start) + '\n'
        return
    return wrapper


def load_data():
    with open('Features.txt', 'rb') as f:
        lst = f.readlines()
    arr_lst = map(lambda x: np.array(eval(x.strip())), lst)
    dataset = np.array(arr_lst)
    return dataset


@timer
def clfter(name, s, x_train, y_train, x_test, y_test,  data, target):
    clf = eval(s)()
    clf.fit(x_train, y_train)
    predict = clf.predict(x_test)
    right = sum(predict == y_test)
    scores = cross_val_score(clf, data, target, cv=5)
    print name + ': '
    print '正确率: %f%%\t' % (right * 100.0 / predict.shape[0]) + ' 交叉验证正确率: %f%%\t' % (
    scores.mean() * 100) + '训练数据: %d\t' % x_train.shape[0] + '测试数据: %d' % x_test.shape[0]
    return



def main():
    clfs = {'多项式朴素贝叶斯': 'MultinomialNB', '支持向量机分类器': 'SVC', 'K邻近分类器': 'KNeighborsClassifier'}
    dataset = load_data()
    data = dataset[:, :12]
    target = dataset[:, 12]
    x_train, x_test, y_train, y_test = train_test_split(data, target, test_size=0.2)
    for clf_name, clf_str in clfs.items():
        clfter(clf_name, clf_str, x_train, y_train, x_test, y_test, data, target)
    return


if __name__ == '__main__':
    main()

