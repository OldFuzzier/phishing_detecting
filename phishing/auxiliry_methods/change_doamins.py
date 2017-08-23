#!/usr/bin/env python
# coding:utf-8

def get_domain():
    with open('top_domain_name.txt', 'rb') as f:
        s = f.read()
    lst = s.split(' ')
    return lst


def change(lst):
    return filter(lambda x: len(x) == 3, lst)


def save_doamain(lst):
    with open('top_domain_name.txt', 'wb') as f:
        for i in lst:
            f.write(i + '\r\n')
    return


def test():
    lst = get_domain()
    new_lst = change(lst)
    print new_lst
    save_doamain(new_lst)