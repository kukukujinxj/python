#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

import os
import sys

import cx_Oracle

reload(sys)
sys.setdefaultencoding('utf8')

os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'


def export(connect, table):
    conn = cx_Oracle.connect(connect, encoding="UTF-8", nencoding="UTF-8")
    c = conn.cursor()
    with open('/opt/oracle/txt/{}.txt'.format(table), 'w') as f:
        x = c.execute('select * from {}'.format(table))
        arr = []
        for row in x:
            cols = []
            for col in row:
                if col:
                    cols.append('\'' + col.decode('utf-8') + '\'')
                else:
                    cols.append('')
            s = '({})'.format(','.join(cols))
            arr.append(s)
        s = 'insert into {0} values {1};'.format(table, ','.join(arr))
        f.write(s)
    c.close()
    conn.close()


