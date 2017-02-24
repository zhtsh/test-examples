#!/usr/bin/python
# coding=utf8

from functools import wraps

# global variable
class MySingletonA(object):
    def foo(self):
        print('foo bar')
instance = MySingletonA()

# __new__
class MySingletonB(object):
    _instance = None
    def __new__(cls, *args, **kargs):
        if not cls._instance:
            cls._instance = super(MySingletonB, cls).__new__(cls, *args, **kargs)
        return cls._instance

class MyClass(MySingletonB):
    def foo(self):
        print('foo bar')

# decorator
def singleton(cls):
    instances = {}
    @wraps(cls)
    def getinstance(*args, **kargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kargs)
        return instances[cls]
    return getinstance

@singleton
class MySingletonC(object):
    def foo(self):
        print('foo bar')

# metaclass
class SingletonMeta(type):
    _instances = {}
    def __call__(cls, *args, **kargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(SingletonMeta, cls).__call__(*args, **kargs)
        return cls._instances[cls]
class MySingletonD(object):
    __metaclass__ = SingletonMeta
    def foo(self):
        print('foo bar')

# class method
class MySingletonE(object):
    @classmethod
    def instance(cls):
        if not hasattr(cls, '_instance'):
            cls._instance = cls('abc')
        return cls._instance

    def __init__(self, param):
        print '__init__'
        print param

    @classmethod
    def initialized(cls):
        return hasattr(cls, '_instance')

    def foo(self):
        print 'hello world'