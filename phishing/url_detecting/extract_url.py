#!/usr/bin/env python
# coding:utf-8

import Queue
import time
from threading import Thread

import urlfeature_util as ft

que_phishing = Queue.Queue(maxsize=5000)
que_normal = Queue.Queue(maxsize=5000)
que_total = Queue.Queue(maxsize=10000)

jobs_phishing = 2
jobs_normal = 1
jobs_consumer = 2


def set_queue(q, filename):
    with open(filename, 'rb') as f:
        lst = f.readlines()
        for i in lst:
            q.put(i)
    return


def task_process(q, flag):
    while True:
        try:
            if q.empty():
                print 'Queue has nothing'
            else:
                url = q.get()
                l = ft.set_feature(url)
                l.append(flag)
                que_total.put(l)
                q.task_done()
        except:
            print 'task has error'
        time.sleep(0.2)


def multi_process(q, task, jobs, flag=None):
    for i in range(1, jobs+1):
        task_i = Thread(target=task, args=(q, flag))
        task_i.setDaemon(True)
        task_i.start()


def task_consumer(q):
    while True:
        try:
            if q.empty():
                print 'Que_Total has nothing'
            else:
                l = q.get()
                with open('Features.txt', 'ab') as f:
                    f.write(str(l)+'\r\n')
                q.task_done()
        except:
            print 'consumer has error'
        time.sleep(0.3)


def multi_consumer(q, task, jobs):
    for i in range(1, jobs+1):
        task_i = Thread(target=task, args=(q, ))
        task_i.setDaemon(True)
        task_i.start()


def test():
    set_queue(que_normal, 'normal_urls.txt')
    set_queue(que_phishing, 'phishing_urls.txt')
    multi_process(que_phishing, task=task_process, jobs=jobs_phishing, flag=2)
    multi_process(que_normal, task=task_process, jobs=jobs_normal, flag=-2)
    multi_consumer(que_total, task=task_consumer, jobs=jobs_consumer)
    que_phishing.join()
    que_normal.join()
    que_total.join()
    print 'MISSION COMPLETE'





