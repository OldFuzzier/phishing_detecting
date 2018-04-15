#!/usr/bin/env python
# coding:utf-8

'''
该模块主要是对URL提取，借助特征化工具特征化，然后存入文件中
'''


import Queue
import time
from threading import Thread

from url_feature import SetFeature


class ExtractURL(object):
    
    def __init__(self):
        self.que_phishing = Queue.Queue(maxsize=5000)
        self.que_normal = Queue.Queue(maxsize=5000)
        self.que_total = Queue.Queue(maxsize=10000)

        self.jobs_phishing = 2
        self.jobs_normal = 1
        self.jobs_consumer = 2

    def set_queue(self, q, filename):
        with open(filename, 'rb') as f:
            lst = f.readlines()
            for i in lst:
                q.put(i)
        return

    def task_process(self, q, flag):
        while True:
            try:
                url = q.get()
                l = SetFeature(url).set_feature()  # 创建SetFeature对象并实现了set_feature方法
                l.append(flag)
                self.que_total.put(l)  # 因为有两组线程同时这个queue中添加，所以有可能造成线程的不安全性(也就是里面所谓的空列表)
                q.task_done()
            except Exception, e:
                print 'TSAK_PROCESS ERROR: %s' % str(e)

    def multi_process(self, q, task, jobs, flag=None):
        for i in range(1, jobs+1):
            task_i = Thread(target=task, args=(q, flag))
            task_i.setDaemon(True)
            task_i.start()

    def task_consumer(self, q):
        while True:
            try:
                l = q.get()
                with open('url_data/features.txt', 'ab') as f:
                    f.write(str(l)+'\n')
                q.task_done()
            except ExtractURL, e:
                print 'TSAK_CONSUMER ERROR: %s' % str(e)

    def multi_consumer(self, q, task, jobs):
        for i in range(1, jobs+1):
            task_i = Thread(target=task, args=(q, ))
            task_i.setDaemon(True)  # 主线程结束就结束
            task_i.start()

    def main(self):
        print '-----------Start to extract URL--------------'
        self.set_queue(self.que_normal, 'url_data/normal_urls.txt')
        self.set_queue(self.que_phishing, 'url_data/phishing_urls.txt')
        self.multi_process(self.que_phishing, task=self.task_process, jobs=self.jobs_phishing, flag=1)
        self.multi_process(self.que_normal, task=self.task_process, jobs=self.jobs_normal, flag=-1)
        self.que_normal.join()
        self.que_phishing.join()
        self.multi_consumer(self.que_total, task=self.task_consumer, jobs=self.jobs_consumer)
        self.que_total.join()  # 阻塞后续程序的运行
        print 'MISSION COMPLETE'


if __name__ == '__main__':
    pass





