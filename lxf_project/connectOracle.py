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


# 10g

# XS_BKS_XJB
export('LWZCXT_EX/Dkff4kaPd1234@166.111.4.168:1521/db1_2', 'XS_BKS_XJB')
# XS_YJS_XJB
export('LWZCXT_EX/Dkff4kaPd1234@166.111.4.168:1521/db1_2', 'XS_YJS_XJB')
# RY_ZZ_JBXX
export('LWZCXT_EX/Dkff4kaPd1234@166.111.4.168:1521/db1_2', 'RY_ZZ_JBXX')

# 12c

# BIZ_UNIT
export('LWZCXT_EX/Dkff4kaPdKK45@166.111.4.250:1521/thu12cpdb', 'BIZ_UNIT')

# DM_GLBM
export('LWZCXT_EX/Dkff4kaPdKK45@166.111.4.250:1521/thu12cpdb', 'DM_GLBM')

# DM_PROJECT_TYPE
export('LWZCXT_EX/Dkff4kaPdKK45@166.111.4.250:1521/thu12cpdb', 'DM_PROJECT_TYPE')

# PAPER_PROJECT
export('LWZCXT_EX/Dkff4kaPdKK45@166.111.4.250:1521/thu12cpdb', 'PAPER_PROJECT')

# PAPER_PROJECT_MEMBER
export('LWZCXT_EX/Dkff4kaPdKK45@166.111.4.250:1521/thu12cpdb', 'PAPER_PROJECT_MEMBER')
