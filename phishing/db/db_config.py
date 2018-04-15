#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
用于mysql数据的相关配置
'''

import os
import MySQLdb

MYSQL_U_P = os.environ.get('MYSQL_USER')
U_P_list = MYSQL_U_P.split(':')
U = U_P_list[0]
P = U_P_list[1]


class MyDB(object):

    def __init__(self):
        self._config = dict(host='127.0.0.1', user=U, passwd=P, db='url_db', charset='utf8')

    def my_select(self, *args):
        conn = MySQLdb.connect(**self._config)
        cur = conn.cursor()
        try:
            cur.execute(*args)
            data = cur.fetchone()
            return data
        except Exception, e:
            print 'db select ERROR: %s' % e
        finally:
            cur.close()
            conn.close()

    def my_select_all(self, *args):
        conn = MySQLdb.connect(**self._config)
        cur = conn.cursor()
        try:
            cur.execute(*args)
            data_tuple = cur.fetchall()
            return data_tuple
        except Exception, e:
            print 'db select ERROR: %s' % e
        finally:
            cur.close()
            conn.close()

    def my_execute(self, sql, params_tup=None):
        conn = MySQLdb.connect(**self._config)
        cur = conn.cursor()
        try:
            if params_tup == None:
                cur.execute(sql)
            else:
                cur.execute(sql, params_tup)
            conn.commit()
        except Exception, e:
            print 'db execute ERROR: %s' % e
            conn.rollback()
        finally:
            cur.close()
            conn.close()

