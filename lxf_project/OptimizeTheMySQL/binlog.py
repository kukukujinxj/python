import queue
import re
import time
from concurrent.futures.thread import ThreadPoolExecutor

import pymysql
from DBUtils.PooledDB import PooledDB


class Binlog(object):
    flag1 = False
    flag2 = False

    def __init__(self):
        self.pool = self.init_pool()
        pass

    def write_sql(self):
        regex = re.compile(r'^(?:select)', re.I)
        s = ''
        for line in open('E:/binlog/pms-slow.log', "r", encoding='gbk', errors='ignore'):
            line = line.strip()
            if line:
                if line[-1] == ';':
                    if s:
                        s += ' ' + line
                    else:
                        s = line
                    if regex.match(s):
                        with open('E:/binlog/select1.txt', 'a') as fw2:
                            s = s.replace("/*!*/;", "").strip()
                            fw2.write(s.strip() + '\n')
                    s = ''
                else:
                    if s:
                        s += ' ' + line
                    else:
                        if regex.match(line):
                            s = line

        # with open('E:/binlog/000539.txt', 'r', encoding='gbk', errors='ignore') as fr1:
        #     line = [i.strip() for i in fr1.readlines()]
        #     i = 0
        #     while i < len(line):
        #         if line[i]:
        #             if line[i][-1] == ';':
        #                 with open('E:/binlog/update.txt', 'a') as fw2:
        #                     if regex.match(line[i]):
        #                         s = line[i].replace("/*!*/;", "").strip()
        #                         fw2.write(s + '\n')
        #                 i += 1
        #             else:
        #                 s = line[i]
        #                 while i + 1 < len(line):
        #                     i += 1
        #                     if line[i]:
        #                         if line[i][-1] == ';':
        #                             with open('E:/binlog/update.txt', 'a') as fw2:
        #                                 s += ' ' + line[i]
        #                                 if regex.match(s):
        #                                     s = s.replace("/*!*/;", "").strip()
        #                                     fw2.write(s.strip() + '\n')
        #                             i += 1
        #                             break
        #                         else:
        #                             s += ' ' + line[i]
        #         else:
        #             i += 1

    def init_pool(self):
        maxconnections = 50  # 最大连接数
        pool = PooledDB(
            pymysql,
            maxconnections,
            host='',
            user='root',
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
            # with open('C:/Users/Administrator/Desktop/process.txt', 'a') as f:
            #     f.write(str(e) + '\n')
            #     f.write(sql + '\n')
            # print(e)
            # print(sql)

    def read_pool(self):
        start = time.time()
        q = queue.Queue()
        # self.producer(q)
        pool = ThreadPoolExecutor(max_workers=32)
        pool.submit(self.producer1, q)
        pool.submit(self.producer2, q)
        for i in range(30):
            pool.submit(self.consumer, q)
        pool.shutdown()
        end = time.time()
        with open('C:/Users/Administrator/Desktop/process.txt', 'a') as f:
            f.write('Task runs %0.2f seconds.\n' % ((end - start),))

    def producer1(self, q):
        for line in open('C:/Users/Administrator/Desktop/select.txt', "r", encoding='gbk', errors='ignore'):
            if line:
                q.put(line)
        self.flag1 = True
        # print("select生产完成")
        # with open('C:/Users/Administrator/Desktop/log2.txt', 'r', encoding='gbk', errors='ignore') as f:
        #     for line in f.readlines():
        #         q.put(line)
        with open('C:/Users/Administrator/Desktop/process.txt', 'a') as f:
            f.write('select生产结束\n')
        # print('生产结束')

    def producer2(self, q):
        for line in open('C:/Users/Administrator/Desktop/update.txt', "r", encoding='gbk', errors='ignore'):
            if line:
                q.put(line)
        self.flag2 = True
        # print("update生产完成")
        with open('C:/Users/Administrator/Desktop/process.txt', 'a') as f:
            f.write('update生产结束\n')

    def consumer(self, q):
        while True:
            if q.empty():
                if self.flag1 and self.flag2:
                    break
                else:
                    # time.sleep(1)
                    continue
            else:
                try:
                    t = q.get(timeout=2)
                    if t:
                        # print(t)
                        self.exe_sql(t)
                except Exception as e:
                    pass
        with open('C:/Users/Administrator/Desktop/process.txt', 'a') as f:
            f.write('消费结束\n')
        # print('消费结束')


if __name__ == "__main__":
    # with open('C:/Users/Administrator/Desktop/process.txt', 'a') as f:
    #     f.write('程序开始\n')
    binlog = Binlog()
    binlog.write_sql()
    # binlog.read_pool()
    # print("结束")
    # with open('C:/Users/Administrator/Desktop/process.txt', 'a') as f:
    #     f.write('程序完结\n')
