#! /usr/bin/python
# encoding: UTF-8

import urllib, urllib2
import cookielib
from BeautifulSoup import BeautifulSoup as BS

class tog:
    def __init__(self, tid):
        self.title = str(tid)
        self.tid = tid
        self.cookie = cookielib.CookieJar()
        self.texts = []
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cookie))

    def call_api(self, name, tid, data):
        url = "http://togetter.com/api/%s/%d" %(name, tid)
        data["csrf_token"] = self.csrf_token
        params = urllib.urlencode(data)
        fp = self.opener.open(url, params)
        return fp.read()

    def get(self, id):
        id = self.tid if id is None else id
        fp = self.opener.open("http://togetter.com/li/%d" %(id))
        html = fp.read()
        soup = BS(html)
        self.csrf_token = soup.find('meta', {"name":"csrf_token"})["content"]
        self.title = soup.find("meta", {"name":"twitter:title"})["content"]
        return html

    def parse2txt(self, html):
        soup = BS(html)
        for i in soup.findAll("div", {"class":"tweet"}):
            self.texts.append(i.text)
        rest = filter(lambda f: f.text.startswith(u"残りを読む"), soup.findAll("a", {"class": "btn comment_btn"}))
        if len(rest) == 1:
            rstr = rest[0]["onclick"]
            page = int(rstr.split(",",1)[1].strip(");"))
            return page
        return None

    def readall(self, id):
        id = self.tid if id is None else id
        html = self.get(id)
        rest = self.parse2txt(html)
        while rest is not None:
            html = self.call_api("moreTweets", self.tid, {"page":rest})
            rest = self.parse2txt(html)
        soup = BS(html)
        rest = filter(lambda f: f.text.startswith(u"次へ"), soup.find('div', {'class' : 'pagenation'}).findAll('a'))
        if len(rest) == 1:
            self.readall(str(rest[0]['href']))


if __name__ == "__main__":
    import sys
    tg = tog(int(sys.argv[1]))
    tg.readall(None)
    titlelen = len(tg.title.encode("EUC-JP"))
    print tg.title.encode("UTF-8")
    print "-"*titlelen
    print ""
    for t in tg.texts:
        print t.encode("UTF-8")
        print ""
