#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import re
import csv

from db_process import MyProcess


class WebPageFeature(object):

    def __init__(self, lst):
        self.phishing_lst = lst
        self._requests = requests

    #  检查请求是否成功
    def get_status(self, html):
        status_code = str(html.status_code)
        print status_code
        if status_code[0] == '2' or status_code[0] == '3':
            return 1
        else:
            return 0

    def get_html(self, url):
        try:
            headers = {'User_Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_1) '
                                     'AppleWebKit/537.36 (KHTML, like Gecko) '
                                     'Chrome/30.0.1581.2 Safari/537.36'}
            html = self._requests.get(url, headers=headers)
            status = self.get_status(html)
            if status:
                text = html.text
                html.encoding = 'utf-8'  # 保证html是utf-8编码（重要）
                print url+' request suecess'
                return text
            else:
                print '4xx or 5xx!'
                return 0
        except:
            print url+' request have error!'
            return 0

    def parser_html(self, html, url, class_):
        soup = BeautifulSoup(html, 'lxml')
        try:
            self.clear_tag(soup, 'script', 'style', 'noscript')  # 去除js和css
            sent_list = [string.lower() for string in soup.stripped_strings if self.match_strings(string)]
            sent_string = '   '.join(sent_list)
            MyProcess().save_sent(url, sent_string, class_)
        except Exception, e:
            print e
            print 'parrser html have error!'
        return

    def match_strings(self, unicode_str):
        pattern = re.compile(ur'\w+?')
        return pattern.search(unicode_str)

    def clear_tag(self, soup, *tags):
        for tag in tags:
            if soup.find(tag):
                map(lambda x: x.clear(), soup.find_all(tag))
            else:
                continue
        return

    # match web page features
    def get_html_params(self, html):
        pass


    def main(self):
        for phishing in self.phishing_lst:
            url = phishing[0]
            class_ = phishing[1]
            html = self.get_html(url)
            if html:
                self.parser_html(html, url, class_)
        return


# 获取钓鱼网址
def readURL():
    with open('verified_online.csv') as csvfile:
        reader = csv.reader(csvfile)  # return是个iterable对象
        url_list = [[row[1], row[-1]] for row in reader][1:]
    return url_list


def test(*url):
    wpf = WebPageFeature([i for i in url])
    wpf.main()


def test_request(url):
    wpf = WebPageFeature([url])
    return wpf.get_html(url)


if __name__ == '__main__':
    pass
