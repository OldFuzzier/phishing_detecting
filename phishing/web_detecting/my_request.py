# coding=utf-8
import time

import requests
from threading import Thread
import Queue
import time


class MyRequest(object):

    def __init__(self):
        super(MyRequest, self).__init__()
        self.request = requests
        self.headers = {'User_Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_1) '
                                         'AppleWebKit/537.36 (KHTML, like Gecko) '
                                         'Chrome/30.0.1581.2 Safari/537.36'}
        self.task_queue = Queue.Queue(maxsize=10000)

    # 基本request
    def request_url(self, url):
        try:
            html = self.request.get(url, headers=self.headers, timeout=5)
            print 'im try to request ' + str(url)
            html.encoding = 'utf-8'
            return html
        except Exception, e:
            print 'request ERROR: ' + str(e)
            return

    #解析html
    def run_parser_html(self, url, parser_func):
        # parser_func 是一个解析html的函数
        html = self.request_url(url)
        text = html.text
        result = parser_func(text)
        return result

    # 线程task
    def m_task(self, func):
        # func指的是task中的具体func
        while True:
            try:
                if self.task_queue.empty():
                    time.sleep(1)
                else:
                    url = self.task_queue.get()
                    html = self.request_url(url)
                    func(html, url)
                    self.task_queue.task_done()
            except Exception, e:
                print 'task ERROR ' + str(e)
            time.sleep(0.3)

    # 装载task
    def load_task(self, *urls):
        for url in urls:
            self.task_queue.put(url)
        return

    # 多线程执行
    def multi_execute(self, n, func):
        # n为启用线程数,
        # func指的是task中的具体func
        for _ in xrange(0, n):
            t = Thread(target=self.m_task, args=(func, ))
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
            return 0



