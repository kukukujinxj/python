import queue
import re
import time
from concurrent.futures.thread import ThreadPoolExecutor

import pymysql
from DBUtils.PooledDB import PooledDB


class Binlog(object):

    def __init__(self):
        self.pool = self.init_pool()
        pass

    def write_sql(self):
        regex = re.compile(r'^(?:insert|update|delete)', re.I)
        with open('C:/Users/Administrator/Desktop/log.txt', 'r', encoding='gbk', errors='ignore') as fr1:
            line = [i.strip() for i in fr1.readlines()]
            i = 0
            while i < len(line):
                if line[i]:
                    if line[i][-1] == ';':
                        with open('C:/Users/Administrator/Desktop/log2.txt', 'a') as fw2:
                            if regex.match(line[i]):
                                s = line[i].replace("/*!*/;", "").strip()
                                fw2.write(s + '\n')
                        i += 1
                    else:
                        s = line[i]
                        while i + 1 < len(line):
                            i += 1
                            if line[i]:
                                if line[i][-1] == ';':
                                    with open('C:/Users/Administrator/Desktop/log2.txt', 'a') as fw2:
                                        s += ' ' + line[i]
                                        if regex.match(s):
                                            s = s.replace("/*!*/;", "").strip()
                                            fw2.write(s.strip() + '\n')
                                    i += 1
                                    break
                                else:
                                    s += ' ' + line[i]
                else:
                    i += 1

    def init_pool(self):
        maxconnections = 50  # 最大连接数
        pool = PooledDB(
            pymysql,
            maxconnections,
            host='',
            user='',
            port=3306,
            passwd='',
            db='',
            use_unicode=True)
        return pool

    def exe_sql(self, sql):
        try:
            con = self.pool.connection()
            cur = con.cursor()
            cur.execute(sql)
            con.commit()
            cur.close()
            con.close()
        except Exception as e:
            pass
            # with open('C:/Users/Administrator/Desktop/log3.txt', 'a') as f:
            #     f.write(str(e) + '\n')
            #     f.write(sql + '\n')
            # print(e)
            # print(sql)

    def read_pool(self):
        start = time.time()
        q = queue.Queue()
        self.producer(q)
        pool = ThreadPoolExecutor(max_workers=32)
        for i in range(32):
            pool.submit(self.consumer, q)
        pool.shutdown()
        end = time.time()
        with open('C:/Users/Administrator/Desktop/log3.txt', 'a') as f:
            f.write('Task runs %0.2f seconds.\n' % ((end - start),))

    def producer(self, q):
        with open('C:/Users/Administrator/Desktop/log2.txt', 'r', encoding='gbk', errors='ignore') as f:
            for line in f.readlines():
                q.put(line)
        with open('C:/Users/Administrator/Desktop/log3.txt', 'a') as f:
            f.write('生产结束\n')
        # print('生产结束')

    def consumer(self, q):
        while True:
            if q.empty():
                break
            else:
                try:
                    t = q.get(timeout=2)
                    if t:
                        self.exe_sql(t)
                except Exception as e:
                    pass
                    # with open('C:/Users/Administrator/Desktop/log3.txt', 'a') as f:
                    #     f.write(str(e) + '\n')
                    # print(e)
        with open('C:/Users/Administrator/Desktop/log3.txt', 'a') as f:
            f.write('消费结束\n')
        # print('消费结束')


if __name__ == "__main__":
    with open('C:/Users/Administrator/Desktop/log3.txt', 'a') as f:
        f.write('程序开始\n')
    binlog = Binlog()
    # binlog.write_sql()
    binlog.read_pool()
    with open('C:/Users/Administrator/Desktop/log3.txt', 'a') as f:
        f.write('程序完结\n')
