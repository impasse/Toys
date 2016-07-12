#!/usr/bin/python3
# encoding:utf-8
from __future__ import unicode_literals


import os
import base64
import sys


def convert(filename):
    with open(filename, 'rb') as r:
        with open(os.path.splitext(filename)[0]) as w:
            base64.encode(r, w)


if __name__ == '__main__':
    if len(sys.argv > 1):
        convert(sys.argv[1])
