#! /usr/bin/env python
# encoding: UTF-8

import requests
import pytest
import requests
from togepub.togetter import Togetter
from togepub.publish import Publisher

@pytest.fixture
def t():
    return Togetter(12345)

def test_init(t):
    assert t.tid == 12345

def test_parse(t):
    res = requests.Response()
    res.status_code = 200
#    res.encoding = 'utf-8'
    with open('test/data/full.html', 'rb') as f:
        res._content = f.read()
#    print(res.content)
    t.parse(res, t.f1)
#    print(t.entries[0])
    pub = Publisher([t])
    pub.publish()


