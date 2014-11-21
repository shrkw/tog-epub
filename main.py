#!/bin/env python
# encoding: UTF-8

from __future__ import division, print_function, absolute_import
import argparse

from togepub import togetter
from togepub import publish

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='from togetter to epub')
    parser.add_argument('tids', type=int, nargs='+', help='should be one tid at least')
    args = parser.parse_args()

    togs = []
    for tid in args.tids:
        tog = togetter.Togetter(tid)
        tog.read()
        togs.append(tog)

    pub = publish.Publisher(togs)
    pub.publish()

