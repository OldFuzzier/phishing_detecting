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

    def __init__(self, url):
        self.NORMAL_BRANDS = self.get_txt('phishing_brands.txt')
        self.SPECIAL_CHARACTER = ['confirm', 'account', 'banking', 'secure', 'ebayisapi', 'webscr', 'login', 'sigin']
        self.url = url
        self.url_structure = urlparse.urlparse(url)

    def get_txt(self, name):
        with open(name, 'rb') as f:
            brands = f.readlines()
            brands_strip = map(lambda x: x.strip(), brands)
            return brands_strip

    '''The following are we need methods'''
    def get_url_domain_symbol_1(self ):
        # url_piece = self.split_url(url)
        symbol = '-'
        domain_lst = list(self.url_structure.netloc)
        if symbol in domain_lst:
            return 1
        else:
            return 0

    def get_url_query_symbol_2(self):
        symbols = ['@', '\?', '\.']
        query = self.url_structure.query
        reg = ''
        for i in symbols:
            reg += '|'+i
        pattern = re.compile(reg[1:])
        if len(pattern.findall(query)) != 0:
            return 1
        else:
            return 0

    def get_url_path_symbol_3(self):
        path = self.url_structure.path
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

    def get_url_length(self):
        point = 85
        point_parameter = 115
        url_len = len(self.url)
        url_piece = self.url_structure
        if url_piece.params != '':
            if url_len >= point_parameter:
                return 1
            else:
                return 0
        else:
            if url_len >= point:
                return 1
            else:
                return 0

    def get_url_domain_length(self):
        point = 39
        if len(self.url_structure.netloc) >= point:
            return 1
        else:
            return 0

    def get_url_domain_level_length(self):
        level = 4
        if self.url_structure.netloc != '':
            if len(self.url_structure.netloc.split('.')) >= level:
                return 1
            else:
                return 0
        else:
            return 0

    def get_url_path_level_length(self):
        level = 6
        if self.url_structure.path != '' or self.url_structure.path != '/':
            if len(self.url_structure.path.split('/'))-1 >= level:  # 因为该len包括了domain
                return 1
            else:
                return 0
        else:
            return 0

    def get_url_domain_is_ip_type(self):
        if self.url_structure.netloc != '':
            for piece in self.url_structure.netloc.split('.'):
                if piece.isdigit():
                    return 1
            else:
                return 0
        return 0

    def get_url_domain_brand(self):
        url_piece = self.url_structure
        for brand in self.NORMAL_BRANDS:
            if url_piece.netloc.find(brand) != -1:
                return 1
        else:
            return 0

    def get_url_path_brand(self):
        url_piece = self.url_structure
        for brand in self.NORMAL_BRANDS:
            if url_piece.path.find(brand) != -1:
                return 1
        else:
            return 0

    def get_url_top_domain_site_error(self):
        pass

    def get_domain_top_in_path(self):
        pass

    def get_tiny_domain(self):
        url_piece = self.url_structure
        point = 7
        if len(url_piece.netloc) <= point:
            return 1
        else:
            return 0

    def get_special_character(self):
        for character in self.SPECIAL_CHARACTER:
            if self.url.find(character) != -1:
                return 1
        else:
            return 0