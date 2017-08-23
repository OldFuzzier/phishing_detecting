#!/usr/bin/env python
# coding:utf-8

import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline

import urlfeature_util as ft

''' Test urls
url1 = "http://www.luxinnerwear.com/javascript_gallery/alibaba/alibaba/login.alibaba.com.php?email=abuse@madecenter.com"
url2 = "http://www.Confirme-paypal.com/"
url3 = "http://www.mmch.co.in/font/index2.html?email=abuse@sfc-ksa.com"
url4 = "http://xxxxx/abc?name=admin&password=admin"
url5 = "http://docs.restala.com/LatestG/file/ServiceLoginAuth.php?cmd=?LOB=RBGLogon&amp;_pageLabel=page_logonform&amp;secured_buyer_page"
url6 = "http://www.legitimate.com//http://www.phishing.com"
url7 = "http://173.236.239.124/wp-content/themes/twentyfourteen/css/alibaba/index.php?email=abuse@houstonlinksmagazine.com"
url8 = "http://www.legitimate.com//http://www.phishing.com"
url9 = "http://www.cclpgms.com/js/?_Acess_Tooken&amp;Acirc;????????????????????????????????792e070ef1e2a9747e63dd241bb32a87792e070ef1e2a9747e63dd241bb32a"
url10 = "http://3designcenter.com/blog/wp-admin/network/other/index.html?.rand&amp;us.battle.net/login/en"
url11 = "http://shop.dominion.dn.ua/templates/redirect/smiles_motivo_para_sorrir_/?https://www.smiles.com.br/promocoes/redireciona/cadastrar/novapromocao/"
url12 = 'https://logn.tabao.com/member/loin.jhtml?redirectURL=http%3A%2F%2Fbuy.tobao.com%2Fauction%2Fbuy_now.htm%3Fphone%3D13718868748%26tccdetailc%3Dwt_one_menu%26action%3Dbuynow%252FPhoneEcardBuyNowAction%26item_id_num%3D9559209412%26from%3Dtcc%26event_submit_do_buy%3D1'
url13 = 'https://auth.alispay.com/logsin/'
'''


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


def test_KNN():
    dataset = load_data()
    data = dataset[:, :12]
    target = dataset[:, 12]
    x_train, x_test, y_train, y_test = train_test_split(data, target, test_size=0.1)
    clf = KNeighborsClassifier(algorithm='kd_tree')
    clf.fit(x_train, y_train)
    return clf


def test():
    KNN_clf = test_KNN()
    for i in range(1, 14):
        url_np = np.array(ft.set_feature(eval('url'+str(i))))
        print KNN_clf.predict(url_np)
    print len(url_np)



