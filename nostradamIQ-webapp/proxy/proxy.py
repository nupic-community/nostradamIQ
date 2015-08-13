#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from cgi import parse_qs
import requests
import base64
import datetime
import redis

#from cache_times import CACHE_MIN # Directory with the TTL for each URL

FILTER = False # only for dev
CACHE_MIN = 5 # only for dev

if FILTER == True:
    with open('urls.txt') as f:
        VALID_URLS = f.read().splitlines()
    f.close()

REDIS = redis.Redis()
def app(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/html'), ('Access-Control-Allow-Origin', '*')])
    parameters = parse_qs(environ.get('QUERY_STRING', ''))
    url = "No url given"
    if 'url' in parameters:
        url = parameters['url'][0]
        valid = True
        if FILTER == True:
            if url not in VALID_URLS:
                valid = False
        if valid:
            return getDocByUrl(url)

    print "ERROR: REQUEST COULD NOT BE MADE!"
    return ""

def getDocByUrl(url):
    cached = False
    ago = datetime.datetime.now() - datetime.timedelta(minutes=CACHE_MIN)
    ago = int((ago-datetime.datetime(1970,1,1)).total_seconds())
    content = REDIS.get(url)
    if content == None:
        req = requests.get(url)
        content = req.content
        date = int((datetime.datetime.now()-datetime.datetime(1970,1,1)).total_seconds())
        REDIS.setex(url,base64.b64encode(content),CACHE_MIN*60) # CACHE_MIN[url]
        print "URL: {0} was inserted in cache with TTL: {1}!".format(url, CACHE_MIN) # CACHE_MIN[url]
    else:
        print "URL: {0} was found in cache!".format(url)
        content = base64.b64decode(content)

    return content

if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    url = ''
    port = 8081
    srv = make_server(url, port, app)
    print "Proxy-Server listening on {0}:{1}".format(url, port)
    srv.serve_forever()