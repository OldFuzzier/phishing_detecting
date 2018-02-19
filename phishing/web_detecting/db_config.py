#!/usr/bin/python
# -*- coding: utf-8 -*-

import MySQLdb


class MyDB(object):

    def __init__(self):
        self._config = dict(host='127.0.0.1', user='root', passwd='wt322426', db='url_db', charset='utf8')

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

    def my_execute(self, sql, params_tup):
        conn = MySQLdb.connect(**self._config)
        cur = conn.cursor()
        try:
            cur.execute(sql, params_tup)
            conn.commit()
        except Exception, e:
            print 'db execute ERROR: %s' % e
            conn.rollback()
        finally:
            cur.close()
            conn.close()

