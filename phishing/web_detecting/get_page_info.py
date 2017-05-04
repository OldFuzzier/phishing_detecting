#!/usr/bin/env python
# coding:utf-8

import requests
from bs4 import BeautifulSoup
import re

# Test URL
URL = 'https://auth.alipay.com/login/index.htm'
URL2 = 'https://login.taobao.com/member/login.jhtml'
URL3 = 'https://passport.jd.com/new/login.aspx'
URL4 = 'https://mybank.icbc.com.cn/icbc/newperbank/perbank3/frame/frame_index.jsp'

# Test HTML
html2 = '''
<html><head><title>The Dormouse's story</title></head>
<script>function a + b</script>
<script>function a + b</script>
<script>function a + b</script>
<p class="title"><b>The Dormouse's story</b></p>
<p class="story">Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
and they lived at the bottom of a well.</p>
<p class="story">...</p>
<style>.aca='12314'</style>d
<style>.aca='12314'</style>d
<style>.aca='12314'</style>d
</html>
'''


class WebPageFeature(object):

    def __init__(self, url):
        self.url = url

    def get_html(self):
        try:
            headers = {'User_Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_1) '
                                     'AppleWebKit/537.36 (KHTML, like Gecko) '
                                     'Chrome/30.0.1581.2 Safari/537.36'}
            text = requests.get(self.url, headers=headers).text
            return text
        except:
            print self.url+' request have error!'
            return 0

    def parser_html(self, html):
        if html:
            soup = BeautifulSoup(html, 'lxml')
            try:
                # 去除js和css
                self.clear_tag(soup, 'script')
                self.clear_tag(soup, 'style')
                vector = [string for string in soup.stripped_strings if self.match_chinese(string)]
                with open('web_page_features3.txt', 'wb') as f:
                    for i in vector:
                        f.write(i.encode('utf-8')+'\r\n')
            except:
                print 'parrser html have error!'

    def match_chinese(self, unicode_str):
        pattern = re.compile(ur'[\u4e00-\u9fa5]+?')
        return pattern.search(unicode_str)

    def clear_tag(self, soup, tag):
        if soup.find(tag):
            return map(lambda x: x.clear(), soup.find_all(tag))
        else:
            return

    # match web page features
    def get_html_params(self, html):
        pass

    def main(self):
        html = self.get_html()
        if html:
            self.parser_html(html)


if __name__ == '__main__':
    wpf = WebPageFeature(URL)



