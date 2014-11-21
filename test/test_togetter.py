#! /usr/bin/env python
# encoding: UTF-8

import requests
import pytest
from togepub.togetter import Togetter

@pytest.fixture
def t():
    return Togetter(12345)

def test_init(t):
    assert t.tid == 12345

def test_parse(t):
    r = requests.Response()
    with open('test/data/full.html', 'r') as f:
        r.__content = ''.join(f.readlines())
    t.parse(r, t.f1)


