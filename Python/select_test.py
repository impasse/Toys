import socket
import select


def gen_sock(addr):
    s = socket.socket()
    s.connect((addr, 80))
    s.send(b'GET / HTTP/1.0\r\nConnection\r\n\r\n')
    return s

readable = select.select([gen_sock('shyling.com'),
                          gen_sock('zyy.cat')],
                         [],
                         [])

print(readable)
