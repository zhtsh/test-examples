#!/usr/bin/python
# coding=utf8

def grep():
    while True:
        line = (yield 1)
        print line

def generateList(start,stop):
	for i in range(start,stop):
		yield i

def countdown(n):
    print "Counting down from", n
    while n >= 0:
        newvalue = (yield n)
        if newvalue is not None:
            n = newvalue
        else:
            n -= 1

if __name__ == '__main__':
    search = grep()
    # activate coroutine
    # next(search)
    # search.send()
    print search.send(None)
    print search.send("I love you")
    print search.send("Don't you love me?")
    print search.send("I love coroutine instead!")
    search.close()

    a = generateList(0, 5)
    for i in range(0, 5):
        print(a.send(None))

    c = countdown(5)
    for x in c:
        print x
        if x == 5:
            c.send(3)
