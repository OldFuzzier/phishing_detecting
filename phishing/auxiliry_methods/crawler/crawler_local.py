#!/usr/bin/env python
# coding:utf-8

import requests
from bs4 import BeautifulSoup
import Queue
from threading import Thread
import time

Q = Queue.Queue(maxsize=1000)
jobs = 10
URL_HOME = 'http://top.chinaz.com/hangyetop/index_hy.html'
URL = 'http://search.top.chinaz.com/top.aspx'
URL_P = 0


def task_load():
    map(lambda x: Q.put(x), range(2, 501))
    return


def main_html(url):
    headers = {'User_Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_1) '
                                 'AppleWebKit/537.36 (KHTML, like Gecko) '
                                 'Chrome/30.0.1581.2 Safari/537.36'}
    try:
        text = requests.get(url, headers=headers).text
    except:
        print 'requests error!'
    try:
        soup = BeautifulSoup(text, 'lxml')
        clearfix_lst = soup.find('div', class_='TopChiList YaHei').find_all('div', class_='ContTit ulli clearfix')
        result_lst = map(lambda x: x.find('div', class_='w320 PCop').find('a')['href'], clearfix_lst)
        result_lst_prefix = map(lambda x: 'www.' + x[x.find('site_') + 5:-5], result_lst)
        with open('local_url_index.txt', 'wb') as f:
            for i in result_lst_prefix:
                f.write(i + '\r\n')
    except:
        print 'parser error!'
'''
-------------------------------------------------------------------
'''


def get_html(url, p):
    try:
        headers = {'User_Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_1) '
                                 'AppleWebKit/537.36 (KHTML, like Gecko) '
                                 'Chrome/30.0.1581.2 Safari/537.36'}
        data = {'p': p, 't': 'hangye'}
        result = requests.get(url, headers=headers, params=data).text
        return result
    except:
        print 'Request failed!'


def parser_html(text):
    try:
        soup = BeautifulSoup(text, 'lxml')
        clearfix_lst = soup.find('div', class_='TopChiList YaHei').find_all('div', class_='ContTit ulli clearfix')
        result_lst = map(lambda x: x.find('div', class_='w320 PCop').find('a')['href'], clearfix_lst)
        result_lst_prefix = map(lambda x: 'www.'+x[x.find('site_')+5:-5], result_lst)
        return result_lst_prefix
    except:
        return []


def task_process(q):
    while True:
        if not q.empty():
            task = q.get()
            try:
                print task
                lst = parser_html(get_html(URL, task))
                with open('local_url.txt', 'ab') as f:
                    if lst == []:
                        print str(task) + ' is empty'
                    else:
                        for i in lst:
                            f.write(i+'\r\n')
            except:
                print str(task) + 'error'
            time.sleep(1)
            q.task_done()
        #else:
            #print 'Queue has nothing!'


def multi_proces(q):
    for i in range(1, jobs+1):
        task_i = Thread(target=task_process, args=(q, ))
        task_i.setDaemon(True)
        task_i.start()


if __name__ == '__main__':
    task_load()
    multi_proces(Q)
    Q.join()
    print 'Have Done'
