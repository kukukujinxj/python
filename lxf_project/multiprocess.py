import os
import random
import time
from multiprocessing import Queue, Process


def run_proc(name):
    print('run child process %s (%s)...' % (name, os.getpid()))


def long_time_task(name):
    print('run task %s (%s)...' % (name, os.getpid()))
    start = time.time()
    time.sleep(random.random() * 3)
    end = time.time()
    print('task %s runs %0.2f seconds' % (name, (end - start)))


def write(q):
    print('process to write: %s' % os.getpid())
    for value in ['A', 'B', 'C']:
        print('put %s to queue...' % value)
        q.put(value)
        time.sleep(random.random())


def read(q):
    print('process to read: %s' % os.getpid())
    while True:
        value = q.get(True)
        print('get %s to queue...' % value)


if __name__ == '__main__':
    print('parent process %s.' % os.getpid())
    # 单个进程
    # p = Process(target=run_proc, args=('test',))
    # print('child process will start.')
    # p.start()
    # p.join()
    # print('child process end')
    # 多进程（进程池）
    # p = Pool(4)
    # for i in range(5):
    #     p.apply_async(long_time_task, args=(i,))
    # print('waiting for all subprocesses done...')
    # p.close()
    # p.join()
    # print('all subprocesses done.')
    # 进程间通信
    q = Queue()
    pw = Process(target=write, args=(q,))
    pr = Process(target=read, args=(q,))
    pw.start()
    pr.start()
    pw.join()
    pr.terminate()
