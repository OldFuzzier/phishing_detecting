#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests
import re

URL = 'http://rmson.com/admin/include/al/gl/dpbx/'


def get_rank(url):
    headers = {'User_Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_1) '
                             'AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/30.0.1581.2 Safari/537.36'}
    try:
        xml = requests.get(url, headers=headers).text
        return re.compile(r'<REACH RANK="\d+"/>').search(xml).group()
    except Exception, e:
        print 'There are not Rank.'
        return 