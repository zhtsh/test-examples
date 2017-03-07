#!/usr/bin/python
# coding=utf8

from singleton import instance
from singleton import MyClass
from singleton import MySingletonC
from singleton import MySingletonD
from singleton import MySingletonE

if __name__ == '__main__':
    print('========global variable=======')
    instance.foo()

    print('')
    print('==========__new__==========')
    a = MyClass()
    b = MyClass()
    a.foo()
    b.foo()
    print(a == b)
    print(a is b)
    print(id(a))
    print(id(b))

    print('')
    print('==========decorator========')
    c = MySingletonC()
    d = MySingletonC()
    c.foo()
    d.foo()
    print(c == d)
    print(c is d)
    print(id(c))
    print(id(d))

    print('')
    print('==========metaclass========')
    e = MySingletonD()
    f = MySingletonD()
    e.foo()
    f.foo()
    print(e == f)
    print(e is f)
    print(id(e))
    print(id(f))

    print('')
    print('===========classmethod========')
    print(MySingletonE.initialized())
    g = MySingletonE.instance()
    print(MySingletonE.initialized())
    g.foo()
    h = MySingletonE.instance()
    h.foo()
    print(g == h)
    print(g is h)
    print(id(g))
    print(id(h))