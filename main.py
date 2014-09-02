#! /usr/bin/env python
# encoding: UTF-8

import togetter
import publish
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='from togetter to epub')
    parser.add_argument('tids', type=int, nargs='+', help='should be one tid at least')
    args = parser.parse_args()

    togs = []
    for tid in tids:
        tog = togetter.Togetter(tid)
        tog.read()
        togs.append(tog)

    pub = publish.Publisher(togs)
    pub.publish()

