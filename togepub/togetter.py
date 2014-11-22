#!/bin/env python
# coding:utf-8

from __future__ import division, print_function, absolute_import
from collections import namedtuple
import requests
from bs4 import BeautifulSoup

Author = namedtuple('Author', ['link', 'name', 'id'])
Tweet = namedtuple('Tweet', ['timestamp', 'link', 'date','text'])
Entry = namedtuple('Entry', ['author', 'tweet'])

class Togetter:

    base_url = "http://togetter.com/"

    def __init__(self, tid):
        self.title = None
        self.tid = tid
        self.entries = []
        self.uri = "%s/li/%d" % (Togetter.base_url, self.tid)

    def __set_title(self, title):
        if self.title is None:
            self.title = title

    def parse(self, r, func):
        r.encoding = 'utf-8'
        soup = BeautifulSoup(r.text)
        for twt in soup.find_all("li", {"class": "list_item"}):
            a = Author(twt.find("a", {"class": "user_link"}).attrs["href"],
                       twt.find("strong").text,
                       twt.find("span", {"class": "status_name"}).text)
            t = Tweet(twt.find("a", {"class": "timestamp"}).attrs["data-timestamp"],
                      twt.find("a", {"class": "timestamp"}).attrs["href"],
                      twt.find("a", {"class": "timestamp"}).text,
                      twt.find("div", {"class": "tweet"}).text)
            self.entries.append(Entry(a, t))
        return func(soup)

    def f1(self, soup):
        self.__set_title(soup.find("meta", {"name": "twitter:title"})["content"])
        self.csrf_token = soup.find('meta', {"name": "csrf_token"})["content"]
        # read more
        return list(filter(lambda f: f.text.startswith(u"残りを読む"), soup.find_all("a", {"class": "btn"})))

    def f2(self, soup):
        # read next page
        pagenation = soup.find('div', {'class': 'pagenation'})
        if pagenation:
            rest = list(filter(lambda f: f.text.startswith(u"次へ"), pagenation.find_all('a')))
            return rest[0]['href']
        else:
            return None

    def read(self, path=None):
        url = self.uri if path is None else "%s/%s" % (Togetter.base_url, path)
        response = requests.get(url)
        cookie = response.cookies.get_dict()
        rest = self.parse(response, self.f1)

        # read more
        if 1 <= len(rest):
            # rstr = rest[0]["onclick"]
            # page = int(rstr.split(",", 1)[1].strip(");"))
            u2 = "%s/api/moreTweets/%d" % (Togetter.base_url, self.tid)
            r2 = requests.post(u2, data={"csrf_token": self.csrf_token}, cookies=cookie)

            next_page = self.parse(r2, self.f2)
            # read next page
            if next_page is not None:
                self.read(next_page)

