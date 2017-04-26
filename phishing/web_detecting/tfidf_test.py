#!/usr/bin/env python
# coding:utf-8

import requests
from bs4 import BeautifulSoup

URL = 'https://www.alipay.com/'


def get_html(url):
    headers = {'User_Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_1) '
                             'AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/30.0.1581.2 Safari/537.36'}
    text = requests.get(url, headers=headers).text
    return text


def parser_html(html):
    soup = BeautifulSoup(html, 'lxml')
    for i in soup.body.descendants:
        yield i


if __name__ == '__main__':
    #gen = parser_html(get_html(URL))
    #for i in gen:
        #print i
    #print get_html(URL)
    html = '''
    <html><head><title>The Dormouse's story</title></head>
    <p class="title"><b>The Dormouse's story</b></p>
    <p class="story">Once upon a time there were three little sisters; and their names were
    <a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
    <a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
    <a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
    and they lived at the bottom of a well.</p>
    <p class="story">...</p>
    </html>
    '''
    for i in parser_html(html):
        print i
        print '-------'

