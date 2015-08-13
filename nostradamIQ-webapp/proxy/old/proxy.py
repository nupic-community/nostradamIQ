#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from flup.server.fcgi import WSGIServer
from cgi import parse_qs
#import requests
import base64
import datetime
from tinydb import TinyDB, where
import urllib
import urllib2
from urlparse import urlparse

FILTER = False
CACHE_MIN = 5


def makeUrlRequest(url):
    user_agent = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0'
    url_parsed = urlparse(url)
    referer = str(url_parsed.scheme) + str(url_parsed.netloc)
    headers = { 'User-Agent' : user_agent,
                'Referer': referer,
                'Access-Control-Allow-Origin': '*' }
    req = urllib2.Request(url, None, headers)
    try:
        response = urllib2.urlopen(req)
        response.headers['Set-Cookie''Access-Control-Allow-Origin'] = '*'
        return response
    except urllib2.URLError as e:
        if hasattr(e, 'reason'):
            print 'We failed to reach a server.'
            print 'Reason: ', e.reason
        elif hasattr(e, 'code'):
            print 'The server couldn\'t fulfill the request.'
            print 'Error code: ', e.code
            return None
        else:
            response = urllib2.urlopen(req)
            response.headers['Set-Cookie''Access-Control-Allow-Origin'] = '*'
            return response 

def app(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/html')])
    parameters = parse_qs(environ.get('QUERY_STRING', ''))
    url = "No URL given"
    if 'url' in parameters:
        url = parameters['url'][0]
        valid = True
        if FILTER == True:
            with open('urls.txt') as f:
                urls = f.read().splitlines()
            if url not in urls:
                print "URL: {0} is not in allowed URLs!\n".format(url) 
                valid = False
        print "Serving URL: {0}\n".format(url)
        if valid:
            return getDocByUrl(url)
    return ""


def getDocByUrl(url):
    cached = False
    db = TinyDB('cache.json')
    ago = int(((datetime.datetime.now() - datetime.timedelta(minutes=CACHE_MIN)) - datetime.datetime(1970,1,1)).total_seconds()) #.timestamp())
    db.remove(where('date') < ago)
    search = db.search((where('url') == url) & (where('date') > ago))
    if len(search) > 0:
        cached = True
        print "URL: {0} was found in cache!\n".format(url)
    if cached:
        return base64.b64decode(search[0]['content'])
    else:
        req = makeUrlRequest(url)
        if req != None: 
            content = req.read()
            date = int((datetime.datetime.now() - datetime.datetime(1970,1,1)).total_seconds()) #.timestamp())
            db.insert({'url':url,'date':date, 'content':base64.b64encode(content)})
            return content
        else:
            print "ERROR: REQUEST COULD NOT BE MADE!\n"
            return ""


#WSGIServer(app).run()

#"""
if __name__ == '__main__':
    url = 'localhost'
    port = 8081
    from wsgiref.simple_server import make_server
    srv = make_server(url, port, app)
    print "Proxy-Server listening on {0}:{1}\n".format(url, port)
    srv.serve_forever()
#"""
