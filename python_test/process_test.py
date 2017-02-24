#!/usr/bin/python
# coding=utf8

import math
import sys

from multiprocessing import Pool
from multiprocessing import Process

def f(x):
    return x*x

#if __name__ == '__main__':
#    p = Pool(5)
#    print(p.map(f, range(100000000)))

def process_fun(num):
    sum = 0
    while(1):
        sum += 1
        p = math.sin(sum * math.pi)
        if sum % 10000 == 0:
            sys.stdout.write('thread-%d: %d\n' % (num, sum))

if __name__ == '__main__':
    for i in range(10):
        print('starting process %d...' % i)
        p = Process(target=process_fun, args=(i,))
        p.start()
    print('all process started')
