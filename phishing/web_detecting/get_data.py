#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
该模块主要用于收集各种web_detecting用的上的数据

'''

import re
import sys
import time
import os

import nltk
from bs4 import BeautifulSoup

out = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(out)
from db.db_process import MyProcess
from my_request import MyRequest

reload(sys)
sys.setdefaultencoding('utf-8')


# 获取URL
class GetURL(MyRequest, MyProcess):
    # 继承 MyRequest 和 MyProcess

    def __init__(self):
        super(GetURL, self).__init__()

    def parser_url(self, html, url):
        pass


# 获取html中的sentence
class GetSent(MyRequest, MyProcess):

    def __init__(self):
        super(GetSent, self).__init__()

    def parser_html(self, html, url, cate):
        text = html.text
        soup = BeautifulSoup(text, 'lxml')
        try:
            print 'start parser' + url
            self.clear_tag(soup, 'script', 'style', 'noscript')  # 去除js和css
            sent_list = [string.lower() for string in soup.stripped_strings if self.match_eng(string)]  # 提取html中的全部英文组成的字符串
            sent_string = ' '.join(sent_list)  # 将每段句子用一个空格连接
            self.save_normal_sent(url, text, sent_string, cate)  # 存入normal_sent_table数据库
            print 'finish parser ' + url
        except Exception, e:
            print 'GetSent.parser_html ERROR ' + str(e)
        return

    # 匹配string中的英文string
    def match_eng(self, unicode_str):
        pattern = re.compile(ur'\w+?')
        return pattern.search(unicode_str)  # 如果匹配不上，返回None


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
        # return filter_word_list
        filter_word_list = []  # 初始化一个过滤词列表
        # ls = LancasterStemmer()  # 初始化词干提取对象
        # english_punctuations = [',', '.', ':', ';', '?', '(', ')', '[', ']', '{', '}', '<', '>', '&', '!', '*', '@',
        #                         '#', '$', '%', '\'', '|', '+', '-', '/', '~', '\\']
        word_list = nltk.word_tokenize(sent)  # 会去除空格, return一个word的列表
        for word in word_list:
            if re.search(r'\W+?', word) or re.search(r'\d+?', word) or len(word)<2:
                # 排除符号数字，只有英文字符, 还有一个英文字母
                # stop_words可以在后续tfidfvector中加入
                continue
            else:
                filter_word_list.append(word)  # 只提取英文词
        return filter_word_list

    # 储存每个html的单词
    def save_page_word(self, flag):
        if flag == 'phish':
            url_sent_all = self.get_phish_sent()[:3000]  # 获取前3000条url以及对应的sentences
            for url_sent in url_sent_all:  # 从数据库取出的是tuple形式, 由url和sentences组成
                url, string_sent, cate= url_sent[0], url_sent[1], url_sent[2]  # 获取出url和sentences和cate
                print 'start save word ' + str(url)
                try:
                    words = self.segment_word(string_sent)
                    string_word = ' '.join(words)  # 一个sent中的words
                    self.save_phish_word(url, string_word, cate)
                    print 'finish save word ' + str(url)
                except Exception, e:
                    print 'segment ERROR ' + str(e)
        elif flag == 'normal':
            url_sent_all = self.get_normal_sent()  # 获取全部url以及对应的sentences
            for url_sent in url_sent_all:  # 从数据库取出的是tuple形式, 由url和sentences组成
                url, string_sent, cate= url_sent[0], url_sent[1], url_sent[2]  # 获取出url和sentences和cate
                print 'start save word ' + str(url)
                try:
                    words = self.segment_word(string_sent)
                    string_word = ' '.join(words)  # 一个sent中的words
                    self.save_normal_word(url, string_word, cate)
                    print 'finish save word ' + str(url)
                except Exception, e:
                    print 'segment ERROR ' + str(e)
        else:
            raise Exception
        return

    def run_phish(self):
        self.save_page_word('phish')
        return

    def run_normal(self):
        self.save_page_word('normal')
        return


# 获取钓鱼网站sentence
class GetPhishSent(GetSent):

    # # 目前不需要标签
    # phish_brands = {'Bank': 'Banking', 'PayPal': 'Banking',
    #                'JPMorgan Chase and Co.': 'Banking', 'Internal Revenue Service': 'Banking', 'Visa': 'Banking',
    #                 'Santander UK': 'Banking',
    #                 'Allegro': 'Game', 'Steam': 'Game',
    #                 'Facebook': 'Social', 'Google': 'Social', 'Orkut': 'Social', 'WhatsApp': 'Social',
    #                 'Dropbox': 'E_Business', 'Microsoft': 'E_Business', 'Apple': 'E_Business', 'Adobe': 'E_Business',
    #                 'eBay, Inc.': 'E_Business',
    #                 'Amazon.com': 'E_Business', 'Alibaba.com': 'E_Business', 'WalMar': 'E_Business',
    #                 'AOL': 'News', 'Yahoo': 'News'}
    
    def __init__(self):
        super(GetPhishSent, self).__init__()

    # # 重写load_task函数(做分类)
    # def load_task(self, *url_brand_list):
    #     for url_brand in url_brand_list:  # url_cate 是url 和 cate组成的tuple
    #         category = self.phish_brands.get(url_brand[1])  # 看看这个brand是否在cate中
    #         if category:
    #             url_brand[1] = category  # 将brand改为category
    #             self.task_queue.put(url_brand)  # task属于一个url和brand组成的tuple
    #         elif 'Bank' in url_brand[1]:
    #             # 第二个是先判断是否有Bank关键字，如果有，直接划分为Banking类型
    #             url_brand[1] = self.phish_brands['Bank']
    #             self.task_queue.put(url_brand)
    #         else:
    #             # 这个url不是所需要的
    #             continue

    # 重写load_task函数
    def load_task(self, *url_brand_list):
        for url_brand in url_brand_list:  # url_cate 是url 和 cate组成的tuple
            self.task_queue.put(url_brand)  # 添加到任务中
        return

    # 重写 parser_html
    def parser_html(self, html, url, cate):
        text = html.text  # 请求网页的html页面
        soup = BeautifulSoup(text, 'lxml')
        try:
            print 'start parser ' + url
            if not soup.find('input'):
                # 如果page中没有input或者form就认为是安全的
                print '%s page have not input or form' % url
            else:
                self.clear_tag(soup, 'script', 'style', 'noscript')  # 去除js和css
                sent_list = [string.lower() for string in soup.stripped_strings if self.match_eng(string)]  # 提取html中的全部英文组成的字符串
                sent_string = ' '.join(sent_list)  # 将每段句子用一个空格连接
                self.save_phish_sent(url, text, sent_string, cate)  # 存入数据库, 结构为 id url html_text, string_sent, cate
                print 'finish parser ' + url
        except Exception, e:
            print 'GetSent.parser_html ERROR ' + str(e)
        return

    # 重写m_task
    def m_task(self, func):
        # func指的是task中的具体func
        while True:
            try:
                url_brand = self.task_queue.get()  # 获取一个url和brand组成的tuple
                html = self.request_url(url_brand[0])  # html是request的对象
                if self.validate_valuable_url(html):  # 验证该url是200
                    func(html, url_brand[0], url_brand[1])
                else:
                    raise Exception('url CODE is 300')  # 就是url是300
            except Exception, e:
                print 'task ERROR ' + str(e)
            finally:
                self.task_queue.task_done()
                time.sleep(0.3)

    # 重写 validate_valuable_url, 不需要 300
    def validate_valuable_url(self, html):
            if html:
                code = str(html.status_code)
                if code[0] == '2':
                    return 1
                else:
                    return 0
            return 0

    def run(self, *url_cate_list):
        self.load_task(*url_cate_list)
        self.multi_execute(10, self.parser_html, task=self.m_task)
        return

    class GetNormalSent(GetSent):

        def __init__(self):
            super(GetNormalSent, self).__init__()

        def load_task(self, *urls):
            # *urls用不上
            url_cate_seq = self.get_normal_url()
            for url_cate in url_cate_seq:
                self.task_queue.put(url_cate)
            return

        # 重写m_task
        def m_task(self, func):
            # func指的是task中的具体func
            while True:
                try:
                    url_cate = self.task_queue.get()  # 获取一个url和cate组成的tuple
                    html = self.request_url(url_cate[0])  # html是request的对象
                    if self.validate_valuable_url(html):  # 验证该url是200或300
                        func(html, url_cate[0], url_cate[1])
                    else:
                        raise Exception('url CODE is 4xx or 5xx')  # 就是url是4xx或者5xx
                except Exception, e:
                    print 'task ERROR ' + str(e)
                finally:
                    self.task_queue.task_done()
                    time.sleep(0.3)

        def parser_html(self, html, url, cate):
            text = html.text
            soup = BeautifulSoup(text, 'lxml')
            try:
                print 'start parser' + url
                self.clear_tag(soup, 'script', 'style', 'noscript')  # 去除js和css
                sent_list = [string.lower() for string in soup.stripped_strings if
                             self.match_eng(string)]  # 提取html中的全部英文组成的字符串
                sent_string = ' '.join(sent_list)  # 将每段句子用一个空格连接
                self.save_normal_sent(url, text, sent_string, cate)  # 存入normal_sent_table数据库
                print 'finish parser ' + url
            except Exception, e:
                print 'GetSent.parser_html ERROR ' + str(e)
            return

        def run(self):
            self.load_task(*[])  # 传入参数没有用
            self.multi_execute(10, self.parser_html, self.m_task)
            return


class GetNormalSent(GetSent):

    def __init__(self):
        super(GetNormalSent, self).__init__()

    def load_task(self, *urls):
        # *urls用不上
        url_cate_seq = self.get_normal_url()
        for url_cate in url_cate_seq:
            self.task_queue.put(url_cate)
        return

    # 重写m_task
    def m_task(self, func):
        # func指的是task中的具体func
        while True:
            try:
                url_cate = self.task_queue.get()  # 获取一个url和cate组成的tuple
                html = self.request_url(url_cate[0])  # html是request的对象
                if self.validate_valuable_url(html):  # 验证该url是200或300
                    func(html, url_cate[0], url_cate[1])
                else:
                    raise Exception('url CODE is 4xx or 5xx')  # 就是url是4xx或者5xx
            except Exception, e:
                print 'task ERROR ' + str(e)
            finally:
                self.task_queue.task_done()
                time.sleep(0.3)

    def parser_html(self, html, url, cate):
        text = html.text
        soup = BeautifulSoup(text, 'lxml')
        try:
            print 'start parser' + url
            self.clear_tag(soup, 'script', 'style', 'noscript')  # 去除js和css
            sent_list = [string.lower() for string in soup.stripped_strings if
                         self.match_eng(string)]  # 提取html中的全部英文组成的字符串
            sent_string = ' '.join(sent_list)  # 将每段句子用一个空格连接
            self.save_normal_sent(url, text, sent_string, cate)  # 存入normal_sent_table数据库
            print 'finish parser ' + url
        except Exception, e:
            print 'GetSent.parser_html ERROR ' + str(e)
        return

    def run(self):
        self.load_task(*[])  # 传入参数没有用
        self.multi_execute(10, self.parser_html, self.m_task)
        return


# 获取Alexa上的URL
class GetAlexaURL(GetURL):
    # 继承了 GetURL

    def __init__(self):
        super(GetAlexaURL, self).__init__()

    # 后去需要的alexa网站
    def get_alexa_url(self):
        url_1 = 'http://alexa.chinaz.com/Country/index_US.html'
        alexa_url_list = []
        alexa_url_list.append(url_1)
        for i in xrange(2, 21):
            url_i = url_1[: -5] + '_%d.html' % i  # http://alexa.chinaz.com/Country/index_US_2.html
            alexa_url_list.append(url_i)
        return alexa_url_list

    # 对alexa网站进行遍历找出其中的url
    def get_url(self):
        url_list = []
        alexa_url_list = self.get_alexa_url()
        for alexa_url in alexa_url_list:
            # 获取每一个alexa网站
            html = self.request_url(alexa_url)
            if self.validate_valuable_url(html):
                soup = BeautifulSoup(html.text, 'lxml')
                li_list = soup.find_all('li', class_='clearfix')
                for li in li_list:
                    a = li.find('a')
                    url = 'http://' + a.string
                    url_list.append(url)
        return url_list

    # 将获取的url存入数据库
    def parser_url(self, html, url):
        # html用来验证
        # url 用来存储
        if self.validate_valuable_url(html):
            self.save_alexa_url(url, 'Nothing')
        return

    def run(self):
        # 加载任务
        url_list = self.get_url()
        self.load_task(*url_list)
        # 多线程执行
        self.multi_execute(5, self.parser_url)  # task就是默认MyRequest.m_task
        return


# 获取Alexa的sentence
class GetNormalURL(GetSent):
    # 因为需要解析html页面，
    # 所以继承GetSent

    def __init__(self):
        super(GetNormalURL, self).__init__()

    def parser_html(self, html, url, cate):
        soup = BeautifulSoup(html.text, 'lxml')
        self.clear_tag(soup, 'script', 'style', 'noscript')  # 去除js和css
        print 'start parser ' + url
        for a_tag in soup.find_all('a'):  # 获取所有a标签
            href_obj = a_tag.get('href')  # 获取a标签的href
            try:
                href = str(href_obj)  # 转换为string格式
                if re.search(r'http://|https://', href):
                    self.save_normal_url(href, cate)
                elif re.search(r'^/\w+?', href):  # 检测每条href中是否有'/yyy/zzz'格式
                    href_new = url + href[1: ]  # 去除第一个'/'
                    self.save_normal_url(href_new, cate)
                else:
                    continue
            except Exception, e:
                # 如果其中有编码错误会被检测出
                print 'encode ERROR: ' + str(e)
        print 'finish parser ' + url
        return

    # 重写load_task
    def load_task(self, *urls):
        # 其中*url用不上，因为数据url从数据库中提取
        url_cate_seq = self.get_alexa_url()
        for url_cate in url_cate_seq:
            self.task_queue.put(url_cate)
        return

    # 重写m_task
    def m_task(self, func):
        # func指的是task中的具体func
        while True:
            try:
                url_cate = self.task_queue.get()  # 获取一个url和cate组成的tuple
                html = self.request_url(url_cate[0])  # html是request的对象
                if self.validate_valuable_url(html):  # 验证该url是200或300
                    func(html, url_cate[0], url_cate[1])
                else:
                    raise Exception('url CODE is 4xx or 5xx')  # 就是url是4xx或者5xx
            except Exception, e:
                print 'task ERROR ' + str(e)
            finally:
                self.task_queue.task_done()
                time.sleep(0.3)

    def run(self):
        self.load_task(*[])  # 传入参数没有用
        self.multi_execute(5, self.parser_html, self.m_task)
        return


if __name__ == '__main__':
    pass