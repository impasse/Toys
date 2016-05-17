#!/usr/bin/env python2
# -*- encoding:utf-8 -*-

from __future__ import print_function, unicode_literals
import socket
import time
import threading

registors = {}


def server():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('0.0.0.0', 20009))
    while True:
        data, addr = sock.recvfrom(1024)
        print('IP:{},PORT:{}'.format(*addr))
        data = data.decode('utf-8')
        if registors.has_key(addr[0]):
            sock.sendto('你已签到'.encode('utf-8'), addr)
        else:
            registors[addr[0]] = data
            sock.sendto('OK', addr)

if __name__ == "__main__":
    s = threading.Thread(target=server)
    s.setDaemon(True)
    s.start()
    while True:
        cmd = raw_input()
        if cmd == "save":
            with open(time.strftime('%Y-%m-%d') + '.csv', 'w+') as save_handle:
                save_handle.write('\r\n'.join(
                    (registors.values())).encode('gbk'))
            print('已保存为{}'.format(save_handle.name))
            break
        if cmd == 'show':
            for k, v in registors.items():
                print("IP:{},{}".format(k, v))
            print('共签到: {}人'.format(len(registors)))
