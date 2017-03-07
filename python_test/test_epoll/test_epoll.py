# coding=utf8

import socket
import select
from datetime import datetime
from datetime import timedelta

EOL = b'\n\n'
response = b'HTTP/1.0 200 OK\nDate: Mon, 1 Jan 1996 01:01:01 GMT\n'
response += b'Content-Type: text/plain\nContent-Length: 13\n\n'
response += b'Hello, world!\n'

# 创建套接字对象并绑定监听端口
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
serversocket.bind(('0.0.0.0', 8080))
serversocket.listen(1)
serversocket.setblocking(0)

# 创建epoll对象，并注册socket对象的 epoll可读事件
epoll = select.epoll()
epoll.register(serversocket.fileno(), select.EPOLLIN)

try:
    connections = {}
    requests = {}
    responses = {}
    while True:
        # 主循环，epoll的系统调用，一旦有网络IO事件发生，poll调用返回。这是和select系统调用的关键区别
        events = epoll.poll(1)
        # 通过事件通知获得监听的文件描述符，进而处理
        for fileno, event in events:
            # 注册监听的socket对象可读，获取连接，并注册连接的可读事件
            if fileno == serversocket.fileno():
                connection, address = serversocket.accept()
                connection.setblocking(0)
                epoll.register(connection.fileno(), select.EPOLLIN)
                connections[connection.fileno()] = connection
                requests[connection.fileno()] = b''
                responses[connection.fileno()] = response
            elif event & select.EPOLLIN:
                # 连接对象可读，处理客户端发生的信息，并注册连接对象可写
                try:
                    requests[fileno] += connections[fileno].recv(1024)
                    if EOL in requests[fileno]:
                        epoll.modify(fileno, event | select.EPOLLOUT)
                        print(requests[fileno])
                except Exception as e:
                    print(e)
                    epoll.unregister(fileno)
                    del connections[fileno]
            elif event & select.EPOLLOUT:
                # 连接对象可写事件发生，发送数据到客户端
                try:
                    byteswritten = connections[fileno].send(responses[fileno])
                    # responses[fileno] = responses[fileno][byteswritten:]
                    # if len(responses[fileno]) == 0:
                    #     epoll.modify(fileno, 0)
                    #     connections[fileno].shutdown(socket.SHUT_RDWR)
                except Exception as e:
                    print(e)
                    # epoll.modify(fileno, 0)
                    epoll.unregister(fileno)
                    del connections[fileno]
            elif event & select.EPOLLHUP:
                epoll.unregister(fileno)
                connections[fileno].close()
                del connections[fileno]
finally:
    epoll.unregister(serversocket.fileno())
    epoll.close()
    serversocket.close()
