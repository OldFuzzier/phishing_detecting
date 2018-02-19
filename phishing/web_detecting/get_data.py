#!/usr/bin/python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import re

import nltk
from nltk.corpus import stopwords
from nltk.stem.lancaster import LancasterStemmer

from db_process import MyProcess
from my_request import MyRequest


# 获取URL
class GetURL(MyRequest, MyProcess):
    # 继承 MyRequest 和 MyProcess
    def __init__(self):
        super(GetURL, self).__init__()

    def get_alexa_url(self):
        url_list = []
        url = 'http://alexa.chinaz.com/Country/index_GB_3.html'
        html = self.request_url(url)
        if html:
            code = html.status_code
            soup = BeautifulSoup(html.text, 'lxml')
            li_list = soup.find_all('li', class_='clearfix')
            for li in li_list:
                a = li.find('a')
                url = 'http://' + a.string
                url_list.append(url)
        return url_list

    # 将获取的url存入数据库
    def url_task(self, html, url):
        # html用来验证
        # url 用来存储
        if self.validate_valuable_url(html):
            self.save_url(url)
        return

    def run(self):
        # 加载任务
        url_list = self.get_alexa_url()
        self.load_task(*url_list)
        # 多线程执行
        self.multi_execute(3, self.url_task)
        return


# 获取html中的sentence
class GetSent(MyRequest, MyProcess):

    def __init__(self):
        super(GetSent, self).__init__()

    def parser_html(self, html, url):
        soup = BeautifulSoup(html.text, 'lxml')
        try:
            print 'start parser' + url
            self.clear_tag(soup, 'script', 'style', 'noscript')  # 去除js和css
            sent_list = [string.lower() for string in soup.stripped_strings if self.match_strings(string)]
            sent_string = ' '.join(sent_list)  # 将每段句子用一个空格连接
            self.save_sent(url, sent_string)
            print 'finish parser ' + url
        except Exception, e:
            print 'GetSent.parser_html ERROR ' + str(e)
        return

    # 匹配string中的英文string
    def match_strings(self, unicode_str):
        pattern = re.compile(ur'\w+?')
        return pattern.search(unicode_str)

    # 清除不需要的标签
    def clear_tag(self, soup, *tags):
        # tags 是一个需要清除tag的list
        for tag in tags:
            if soup.find(tag):
                map(lambda x: x.clear(), soup.find_all(tag))
            else:
                continue
        return

    # match web page features
    def get_html_params(self, html):
        pass


    def run(self, *url_list):
        # url_list 是需要请求的url列表
        self.load_task(*url_list)
        self.multi_execute(3, self.parser_html)
        return


# 将sentence转换为word
class GetWord(MyProcess):
    
    def __init__(self):
        super(GetWord, self).__init__()

    # 分割sentence
    def segment_word(self, sent):
        ls = LancasterStemmer()  # 初始化词干提取对象
        english_punctuations = [',', '.', ':', ';', '?', '(', ')', '[', ']', '&', '!', '*', '@', '#', '$', '%', '\'',
                                '|', '+', '-']
        words = nltk.word_tokenize(sent)
        filter_words = filter(lambda x: x not in english_punctuations and x not in stopwords.words('english'), words)
        stem_words = map(lambda x: ls.stem(x), filter_words)  # 提取词干
        return stem_words

    # 储存每个html的单词
    def save_page_word(self):
        url_sents_all = self.get_sent()  # 获取全部url以及对应的sentences
        for url_sents in url_sents_all:  # 从数据库取出的是tuple形式, 由url和sentences组成
            url, sents_string = url_sents[0], url_sents[1]  # 获取出url和sentences
            words_lst = []  # 每一个sents分解成分解成word后组成的list
            sents_lst = sents_string.split(' ')  # 将sents的string变成list
            print 'start save word ' + str(url)
            for sent in sents_lst:  # 从一个sents的list中进行遍历
                words = self.segment_word(sent)
                word_string = ' '.join(words)  # 一个sent中的words
                words_lst.append(word_string)  # 添加到全部sents中的words_list中
            words_string = ' '.join(words_lst)  # 将worlds_list 装换位 words_string
            self.save_word(url, words_string)
            print 'finish save word ' + str(url)
        return




if __name__ == '__main__':
    pass