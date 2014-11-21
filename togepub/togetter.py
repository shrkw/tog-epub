#!/bin/env python
# coding:utf-8

from __future__ import division, print_function, absolute_import
import requests
from bs4 import BeautifulSoup

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
        for tweet in soup.find_all("div", {"class": "tweet"}):
            self.entries.append(tweet.text)
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

