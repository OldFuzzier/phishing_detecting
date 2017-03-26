#!/usr/bin/env python
# coding:utf-8

import urlparse
import re


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
    'get_tiny_domain'
]


def get_txt(name):
    with open(name, 'rb') as f:
        brands = f.readlines()
        brands_strip = map(lambda x: x.strip(), brands)
        return brands_strip


def split_url(url):
    return urlparse.urlparse(url)


NORMAL_BRANDS = get_txt('phishing_brands.txt')
# TOP_DOMAINS = get_txt('top_domain_name')
'''
------------------------------------------------------------
'''


def get_url_domain_symbol_1(url):
    url_piece = split_url(url)
    symbol = '-'
    domain_lst = list(url_piece.netloc)
    if symbol in domain_lst:
        return 1
    else:
        return 0


def get_url_query_symbol_2(url):
    url_piece = split_url(url)
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


def get_url_path_symbol_3(url):
    symbol1 = '//'
    symbol2 = '\.'
    pattern1 = re.complie(symbol1)
    pattern2 = re.complie(symbol2)
    if len(pattern1.findall(url)) > 1:
        return 1
    elif len(pattern2.findall(url)) > 0:
        return 1
    else:
        return 0


def get_url_length(url):
    point = 85
    point_paramter = 115
    url_len = len(url)
    url_piece = split_url(url)
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


def get_url_domain_length(url):
    point = 39
    url_piece = split_url(url)
    if len(url_piece.netloc) >= point:
        return 1
    else:
        return 0


def get_url_domain_level_length(url):
    level = 4
    url_piece = split_url(url)
    if url_piece.netloc != '':
        if len(url_piece.netloc.split('.')) >= level:
            return 1
        else:
            return 0
    else:
        return 0


def get_url_path_level_length(url):
    level = 6
    url_piece = split_url(url)
    if url_piece.path != '' or url_piece.path != '/':
        if len(url_piece.path.split('/'))-1 >= level:  # 因为该len包括了domain
            return 1
        else:
            return 0
    else:
        return 0


def get_url_domain_is_ip_type(url):
    url_piece = split_url(url)
    if url_piece.netloc != '':
        for piece in url_piece.netloc.split('.'):
            if piece.isdigital():
                return 1
        else:
            return 0
    return 0


def get_url_domain_brand(url):
    url_piece = split_url(url)
    reg = ''
    for i in NORMAL_BRANDS:
        reg += '|'+i
    pattern = re.compile(reg[1:])
    if len(pattern.findall(url_piece.netloc)) != 0:
        return 1
    else:
        return 0


def get_url_path_brand(url):
    url_piece = split_url(url)
    reg = ''
    for i in NORMAL_BRANDS:
        reg += '|'+i
    pattern = re.compile(reg[1:])
    if len(pattern.findall(url_piece.path)) != 0:
        return 1
    else:
        return 0


def get_url_top_domain_site_error(url):
    pass


def get_domain_top_in_path(url):
    pass


def get_tiny_domain(url):
    url_piece = split_url(url)
    point = 7
    if len(url_piece.netloc) <= point:
        return 1
    else:
        return 0



