
from urllib2 import urlopen, Request
from urllib import urlencode
import calendar
import datetime
import os
import re

class Reader(object):
    BASE = "https://www.google.com"
    LOGIN = "/accounts/ClientLogin"
    FEED = "http://www.google.com/reader/atom/feed/%s"

    CONT_PTN = re.compile("<gr:continuation>(.+)</gr:continuation>")
    def __init__(self, credentials):
        data = urlencode((
                ('Email', credentials[0]),
                ('Passwd', credentials[1]),
                ('service', 'reader')
            ))
        req = Request(Reader.BASE + Reader.LOGIN, data=data)
        res = urlopen(req)
        content = res.read()
        authDict = dict(x.split('=') for x in content.split('\n') if x)
        AUTH = authDict["Auth"]
        self.headers = {"Authorization" : "GoogleLogin auth=%s"%AUTH}
       
    def getFeed(self, feedUrl):
        url = Reader.FEED % feedUrl + "?n=20"
        return self._get(url)

    def getFeedItemsAfter(self, feedUrl, afterDate=None, cont=None):
        url = Reader.FEED % feedUrl
        
        if cont:
            url += "?r=o" + "&c=%s" % cont
        elif afterDate:
            dateStr = calendar.timegm(afterDate.utctimetuple())
            url += "?r=o" + "&ot=%s" % dateStr
        return self._get(url)

    def getContinuation(self, content):
        match = Reader.CONT_PTN.search(content)
        if match:
            return match.group(1)
        return None

    def _get(self, url):
        req = Request(url)
        self.addHeaders(req)
        return urlopen(req)

    def addHeaders(self, req):
        for key, val in self.headers.items():
            req.add_header(key, val)

def getCredentials():
    "read a two line credential file in this dir"
    path = os.path.join(os.path.dirname(__file__), "credentials.txt")
    with open(path) as f:
        lines = f.readlines()
    return lines[0].strip(), lines[1].strip()

