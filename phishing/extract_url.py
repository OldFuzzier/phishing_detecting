#!/usr/bin/env python
# coding:utf-8

import pandas as pd


df = pd.read_csv('verified_online.csv')
lst = []
print df.loc[:3, ['url']]

