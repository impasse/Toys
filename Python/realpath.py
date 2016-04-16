#!/usr/bin/env python2
# -*- encoding:utf-8 -*-

from __future__ import print_function
import os
import sys

def main(filename):
    if filename is None:
        print(os.getcwd())
    else:
        print(os.path.realpath(filename))


if __name__ == '__main__':
    main(len(sys.argv) > 1  and sys.argv[1] or None)
