from __future__ import unicode_literals
import sys


def crack(imei):
    k = i = j = 0
    n = len(imei)
    while j < n:
        if j < 5 or j >= n - 5:
            c = ord(imei[j]) & 0xff
            k = (k + (((((0xc1e3 * c) & 0xffff) >> 1) - c) & 0xffff)) & 0xffff
            i += 1
        j += 1
    return 0xffff & k

if __name__ == '__main__':
    if len(sys.argv)>1:
        print(crack(sys.argv[1]))
    else:
        print('Usage: {} IMEI'.format(sys.argv[0]))
