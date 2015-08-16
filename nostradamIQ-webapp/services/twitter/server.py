#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# serves the twitter files in redis via REST API on URL:8088

from cgi import parse_qs
import requests
import datetime
import os
import os.path
import redis
import json

REDIS = redis.Redis()

# Format:
# HOUR = HH (str)
# DATE = DD-MM-YYYY (str)
# ARRAY = key for keywords Dict that contains filterwords for twitter stream object (str)
# tweets_ARRAY_HOUR_DATE.geojson -> geoJSON object to be read by Cesium
# stats_ARRAY_HOUR_DATE -> ((ALL, WITH_GEO), (ALL_INTV, WITH_GEO_INTV))

def app(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/html'), ('Access-Control-Allow-Origin', '*')])
    parameters = parse_qs(environ.get('QUERY_STRING', ''))
    filename = "No filename given"
    if 'file' in parameters:
        filename = parameters['file'][0]
        response = REDIS.get(filename)
        if response != None:
            return response
        else:
            # retrieve geoJSON file: # ONLY IF WE DON'T DELETE THEM!
            if os.path.isfile(filename):
                with open(filename, 'r') as responseFile:
                    response = json.loads(responseFile)
                responseFile.close()
                if response != None:
                    return response	
        print "ERROR: FILE NOT FOUND!\n"
        return ""
    print "ERROR: REQUEST COULD NOT BE MADE!\n"
    return ""

if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    url = ''
    port = 8088
    srv = make_server(url, port, app)
    print "Twitter-Server listening on {0}:{1}\n".format(url, port)
    srv.serve_forever()