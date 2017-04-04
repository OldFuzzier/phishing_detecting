#!/usr/bin/env python
# coding:utf-8

import requests
from bs4 import BeautifulSoup
import Queue
from threading import Thread
import time

Q = Queue.Queue(maxsize=50)
jobs = 5
URL = 'http://alexa.chinaz.com/Global/index.html'
url_db = []


def task_load():
    Q.put(URL)
    for i in range(2, 21):
        url_i = URL[:-5]+'_%d.html' % i
        Q.put(url_i)
    return
'''
-------------------------------------------------------------------------------------
'''

def get_html(url):
    headers = {'User_Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_1) '
                             'AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/30.0.1581.2 Safari/537.36'}
    result = requests.get(url, headers=headers).text
    return result


def parser_html(text):
    try:
        soup = BeautifulSoup(text, 'lxml')
        ul_list = soup.find('ul', class_='rowlist').find_all('li', class_='clearfix')
        a_list = map(lambda x: x.find('a', class_='tohome')['href'], ul_list)
        return a_list
    except:
        return []


def task_process(q):
    while True:
        if not q.empty():
            task = q.get()
            try:
                url_lst = parser_html(get_html(task))
                print task
                url_db.append(url_lst)
            except:
                print task + 'error'
            time.sleep(0.5)
            q.task_done()


def multi_process(q):
    for i in range(1, jobs+1):
        task_i = Thread(target=task_process, args=(q,))
        task_i.setDaemon(True)
        task_i.start()


if __name__ == '__main__':
    task_load()
    multi_process(Q)
    Q.join()
    print len(url_db)
    print url_db
