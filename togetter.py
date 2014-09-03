#! /usr/bin/env python
# encoding: UTF-8

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

    def read(self, path=None):
        url = self.uri if path is None else "%s/%s" % (Togetter.base_url, path)
        response = requests.get(url)
        cookie = response.cookies.get_dict()

        def parse(r, func):
            r.encoding = 'utf-8'
            soup = BeautifulSoup(r.text)
            for tweet in soup.find_all("div", {"class": "tweet"}):
                self.entries.append(tweet.text)
            return func(soup)

        def f1(soup):
            self.__set_title(soup.find("meta", {"name": "twitter:title"})["content"])
            self.csrf_token = soup.find('meta', {"name": "csrf_token"})["content"]
            # read more
            return list(filter(lambda f: f.text.startswith(u"残りを読む"), soup.find_all("a", {"class": "btn"})))

        rest = parse(response, f1)

        # read more
        if len(rest) == 1:
            # rstr = rest[0]["onclick"]
            # page = int(rstr.split(",", 1)[1].strip(");"))
            url = "%s/api/moreTweets/%d" % (Togetter.base_url, self.tid)
            r2 = requests.post(url, data={"csrf_token": self.csrf_token}, cookies=cookie)

            def f2(soup):
                # read next page
                pagenation = soup.find('div', {'class': 'pagenation'})
                if pagenation:
                    rest = list(filter(lambda f: f.text.startswith(u"次へ"), pagenation.find_all('a')))
                    return rest[0]['href']
                else:
                    return None

            next_page = parse(r2, f2)
            # read next page
            if next_page is not None:
                self.read(next_page)

