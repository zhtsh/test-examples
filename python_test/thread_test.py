#!/usr/bin/python
# coding=utf8

import threading
import math
import sys

def thread_fun(num):
    sum = 0
    while(1):
        sum += 1
        p = math.sin(sum * math.pi)
        if sum % 1000000 == 0:
            sys.stdout.write('%s: %d\n' % (threading.currentThread().name, sum))
            break

if __name__ == '__main__':
    threads = []
    for i in range(10):
        print('starting thread %d...' % i)
        thread_name = 'thread-%d' % i
        t = threading.Thread(target=thread_fun, name=thread_name, args=(i,))
        t.start()
        threads.append(t)
    print('all thread started')
    for t in threads:
        t.join()
        print('%s: returned' % t.name)
    print('all thread finished')
