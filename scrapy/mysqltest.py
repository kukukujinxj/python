#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' a mysql test '

# 导入MySQL驱动:
import mysql.connector

config = {
    'host': '112.74.19.176',
    'user': 'power_ad',
    'password': 'codespace0@#$',
    'port': '3306',
    'database': 'ad_guider',
    'charset': 'utf8'

    # 'host': '127.0.0.1',
    # 'user': 'root',
    # 'password': '123456',
    # 'port': '3306',
    # 'database': 'ad_guider',
    # 'charset': 'utf8'
}


def execute(sql_cmd, param, flag):
    """
    :param sql_cmd sql 命令
    :param param 参数
    """
    try:
        # 注意把password设为你的root口令:
        conn = mysql.connector.connect(**config)
    except mysql.connector.Error as e:
        print('connect fails!{}'.format(e))
    cursor = conn.cursor()
    try:
        cursor.execute(sql_cmd, param)
        if 'insert' == flag:
            ret = cursor.rowcount
        else:
            ret = cursor.fetchall()
    except mysql.connector.Error as e:
        print('sql execute fails!{}'.format(e))
    else:
        return ret
    finally:
        cursor.close()
        conn.commit()


if __name__ == '__main__':
    sql_cmd = 'INSERT INTO ad_guider.ad_label(laTitle) VALUES(%s)'
    param = ('好的',)
    ret = execute(sql_cmd, param, 'insert')
    print(ret)
    sql_cmd = 'SELECT * FROM ad_guider.ad_label WHERE laId = %s'
    param = ('321',)
    ret = execute(sql_cmd, param, 'select')
    print(ret)

# # 注意把password设为你的root口令:
# conn = mysql.connector.connect(**config)
# cursor = conn.cursor()
# # 插入一行记录，注意MySQL的占位符是%s:
# cursor.execute('INSERT INTO ad_guider.ad_label(laTitle) VALUES(%s)', ['好的'])
# print(cursor.rowcount)
# # 提交事务:
# conn.commit()
# cursor.close()
# # 运行查询:
# cursor = conn.cursor()
# cursor.execute('SELECT * FROM ad_guider.ad_label WHERE laId = %s', ('321',))
# values = cursor.fetchall()
# print(values)
# cursor.close()
# conn.commit()
