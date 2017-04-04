#!/usr/bin/env python
# coding:utf-8

import re
import urlparse

features_lst = [
    'get_url_domain_-(symbol1)',
    'get_url_query_@?(symbol2)',
    'get_url_path_//.(symbol3)',
    'get_url_length',
    'get_url_domain_length',
    'get_url_domain_level_length',
    'get_url_path_level_length',
    'get_url_domain_is_ip_type',
    'get_url_domain_brand',
    'get_url_path_brand',
    'get_url_top_domain_site_error(give up)',
    'get_domain_top_in_path(give up)',
    'get_tiny_domain',
    'get_special_character'
]

#NORMAL_BRANDS = get_txt123('phishing_brands.txt')
# TOP_DOMAINS = get_txt('top_domain_name.txt')
'''
------------------------------------------------------------
'''


class FeatureClassify(object):

    def __init__(self):
        self.NORMAL_BRANDS = self.get_txt('phishing_brands.txt')
        self.SPECIAL_CHARACTER = ['confirm', 'account', 'banking', 'secure', 'ebayisapi', 'webscr', 'login', 'sigin']

    def get_txt(self, name):
        with open(name, 'rb') as f:
            brands = f.readlines()
            brands_strip = map(lambda x: x.strip(), brands)
            return brands_strip

    def split_url(self, url):
        return urlparse.urlparse(url)
    '''
    The following are we need methods
    '''
    def get_url_domain_symbol_1(self, url):
        url_piece = self.split_url(url)
        symbol = '-'
        domain_lst = list(url_piece.netloc)
        if symbol in domain_lst:
            return 1
        else:
            return 0

    def get_url_query_symbol_2(self, url):
        url_piece = self.split_url(url)
        symbols = ['@', '\?', '\.']
        query = url_piece.query
        reg = ''
        for i in symbols:
            reg += '|'+i
        pattern = re.compile(reg[1:])
        if len(pattern.findall(query)) != 0:
            return 1
        else:
            return 0

    def get_url_path_symbol_3(self, url):
        url_piece = self.split_url(url)
        path = url_piece.path
        symbol1 = '//'
        symbol2 = '\.'
        pattern1 = re.compile(symbol1)
        pattern2 = re.compile(symbol2)
        if len(pattern1.findall(path)) > 1:
            return 1
        elif len(pattern2.findall(path)) > 0:
            return 1
        else:
            return 0

    def get_url_length(self, url):
        point = 85
        point_paramter = 115
        url_len = len(url)
        url_piece = self.split_url(url)
        if url_piece.params != '':
            if url_len >= point_paramter:
                return 1
            else:
                return 0
        else:
            if url_len >= point:
                return 1
            else:
                return 0

    def get_url_domain_length(self, url):
        point = 39
        url_piece = self.split_url(url)
        if len(url_piece.netloc) >= point:
            return 1
        else:
            return 0

    def get_url_domain_level_length(self, url):
        level = 4
        url_piece = self.split_url(url)
        if url_piece.netloc != '':
            if len(url_piece.netloc.split('.')) >= level:
                return 1
            else:
                return 0
        else:
            return 0

    def get_url_path_level_length(self, url):
        level = 6
        url_piece = self.split_url(url)
        if url_piece.path != '' or url_piece.path != '/':
            if len(url_piece.path.split('/'))-1 >= level:  # 因为该len包括了domain
                return 1
            else:
                return 0
        else:
            return 0

    def get_url_domain_is_ip_type(self, url):
        url_piece = self.split_url(url)
        if url_piece.netloc != '':
            for piece in url_piece.netloc.split('.'):
                if piece.isdigit():
                    return 1
            else:
                return 0
        return 0

    def get_url_domain_brand(self, url):
        url_piece = self.split_url(url)
        for brand in self.NORMAL_BRANDS:
            if url_piece.netloc.find(brand) != -1:
                return 1
        else:
            return 0

    def get_url_path_brand(self, url):
        url_piece = self.split_url(url)
        for brand in self.NORMAL_BRANDS:
            if url_piece.path.find(brand) != -1:
                return 1
        else:
            return 0

    def get_url_top_domain_site_error(self, url):
        pass

    def get_domain_top_in_path(self, url):
        pass

    def get_tiny_domain(self, url):
        url_piece = self.split_url(url)
        point = 7
        if len(url_piece.netloc) <= point:
            return 1
        else:
            return 0

    def get_special_character(self, url):
        for character in self.SPECIAL_CHARACTER:
            if url.find(character):
                return 1
        else:
            return 0
