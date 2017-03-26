#!/usr/bin/env python
# coding:utf-8

def get_brands():
    with open('brands.txt', 'rb') as f:
        lst = f.readlines()
    return lst


def save_brands(lst):
    with open('phishing_brands.txt', 'wb') as f:
        for i in lst:
            f.write(i + '\r\n')
    return


def change_lst(lst):
    lst_new = []
    for row in lst:
        row_lst = row.split(' ')
        if len(row_lst) > 2:
            lst_new.append(''.join([word[0].lower() for word in row_lst]))
        if len(row_lst) == 2:
            lst_new.append(row_lst[0].lower())
        else:
            lst_new.append(row_lst[0].lower().strip())
    return lst_new


if __name__ == '__main__':
    lst = get_brands()
    new_lst = change_lst(lst)
    save_brands(new_lst)
