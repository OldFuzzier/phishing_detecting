# coding=utf-8

'''
该模块用于phishing_detecting所有任务的网络请求
'''

import requests
from threading import Thread
import Queue
import time


class MyRequest(object):
    # multiple request
    # step1: load_task
    # step2: multi_execute

    def __init__(self):
        super(MyRequest, self).__init__()
        self.request = requests
        self.headers = {'User_Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_1) '
                                         'AppleWebKit/537.36 (KHTML, like Gecko) '
                                         'Chrome/30.0.1581.2 Safari/537.36'
                        }
        self.task_queue = Queue.Queue(maxsize=100050)

    # 基本request
    def request_url(self, url, params=None, cookies=None):
        try:
            html = self.request.get(url, headers=self.headers, timeout=3, params=params, verify=False, cookies=cookies)
            print u'im try to request ' + unicode(url)
            html.encoding = 'utf-8'
            return html
        except Exception, e:
            print u'request ERROR: ' + unicode(e)
            return

    # 线程task
    def m_task(self, func):
        # func指的是task中的具体func
        while True:
            try:
                # if self.task_queue.empty():
                #     time.sleep(1)
                # else:
                url = self.task_queue.get()
                html = self.request_url(url)
                func(html, url)
                self.task_queue.task_done()
                time.sleep(0.3)
            except Exception, e:
                print 'task ERROR ' + str(e)

    # 装载task
    def load_task(self, *urls):
        for url in urls:
            self.task_queue.put(url)
        print 'Load finish'
        return

    # 多线程执行
    def multi_execute(self, n, func, task=None):
        # n为启用线程数,
        # func指的是task中的具体func
        # task 指的是执行的任务默认为 self.m_task(目的是解耦)
        if task == None:
            task = self.m_task
        for _ in xrange(0, n):
            t = Thread(target=task, args=(func, ))
            t.setDaemon(True)  # 主线程结束就结束
            t.start()
        self.task_queue.join()  # 等待任务队列结束
        print 'task_queue Done!'
        return

    # 验证request的url有效性
    def validate_valuable_url(self, html):
            if html:
                code = str(html.status_code)
                if code[0] == '2' or code[0] == '3':
                    return 1
                else:
                    return 0
            raise HttpRequestError()

    # 这是一个类的装饰器, 就是检验状态码的
    @staticmethod
    def validate_html(func):
        def inner(self, html, *args, **kwargs):
            if html:
                code = str(html.status_code)
                if code[0] == '2' or code[0] == '3':
                    return func(self, html, *args, **kwargs)
                else:
                    raise HttpRequestError()
            raise HttpRequestError()
        return inner

    # 测试请求+解析html(test)
    def run_parser_html(self, url, parser_func):
        # parser_func 是一个解析html的函数
        html = self.request_url(url)
        text = html.text
        result = parser_func(text)
        return result


# 自定义了一个请求的错误
class HttpRequestError(Exception):

    def __init__(self):
        super(HttpRequestError, self).__init__()
    
    def __str__(self):
        return 'Reqeust ERROR: your status_code is not 2xxx or 3xx.'
