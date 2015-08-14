#!/usr/bin/python
# -*- coding: utf-8 -*-

# http://tweepy.readthedocs.org/en/v3.2.0/streaming_how_to.html?highlight=stream

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json
import re
import time
import datetime
import sys
import os
import redis

from tweet2geoJSON import format2geoJSON
from httplib import IncompleteRead

from API_KEYS import consumer_key, consumer_secret, access_token, access_token_secret

REDIS = redis.Redis()

# Delete old file?
DELETE_OLD = False

countAll = 0
countLoc = 0
countAll_intervall = 0 
countLoc_intervall = 0

# holds the name of the searcharray
searchArray = None

 # tweets_ARRAY_HOUR_DATE.geojson
outputgeo_tpl = "tweets_%s_%s_%s.geojson"
# name of current file:
outputgeo = None

nowDateTime = getCurrentDateKey()
currentKeyDateTime = None

# https://dev.twitter.com/rest/public/search
KEYWORDS = {
        'quake': ["#earthquake", "#quake", "#shakeAlert", "#quakeAlert", "shakeAlert", "quakeAlert", "earthquake", "quake", "from:USGSted", "from:everyEarthquake"]
}


def getCurrentDateKey():
    # Returns: str: HH:DD-MM-YYYY 
    hour = datetime.datetime.now().hour
    date = "{0}-{1}-{2}".format(datetime.datetime.now().day,datetime.datetime.now().month, datetime.datetime.now().year)
    return "{0}:{1}".format(hour, date)

class StdOutListener(StreamListener):

    def on_data(self, data):
        global countLoc, countAll, countAll_intervall, countLoc_intervall, outputgeo, nowDateTime

        # update nowDateTime:
        nowDateTime = getCurrentDateKey()

        try:
            tweet = json.loads(data)
            print('@%s tweeted: %s\nPlace: %s (%s)\n' % ( tweet['user']['screen_name'], tweet['text'], tweet['place'], tweet['coordinates']))
            countAll += 1
            countAll_intervall += 1
            # convert to and write as .geoJSON:
            geoJson = format2geoJSON(tweet)
            if geoJson != None:
                # TODO write in Redis Proxy instance
                with open(outputgeo, 'a+') as outPgeo:
                    json.dump(geoJson, outPgeo)
                    outPgeo.write(',')
                outPgeo.close()
                countLoc += 1
                countLoc_intervall += 1
            if countAll%100 == 0:
                print "Saw {0} tweets; {1} of them had location information!\n".format(countAll, countLoc)

        except: pass

        return True

    def on_error(self, status):
        print 'Error: ', status

if __name__ == '__main__':
    # Get SysArgs and the keyword array:
    searchArray = sys.argv[1:]
    try: 
        keywordArray = KEYWORDS[searchArray]
    except:
        print "keywordArray with the name {0} does not exsist!\n".format(searchArray)
        exit(0)
  
    while nowDateTime == currentKeyDateTime: # Changes every hour, so that we publish hourly
        try:
            l = StdOutListener()
            auth = OAuthHandler(consumer_key, consumer_secret)
            auth.set_access_token(access_token, access_token_secret)
            stream = Stream(auth, l)
            stream.filter(track=keywordArray)#, async=True) #async for multithreating
        except KeyboardInterrupt:
            print "\n\nYOU INTERRUPTED!\nFINISH WRITING FILE\n"
            print "Saw {0} tweets; {1} of them had location information!\n".format(countAll, countLoc)
            with open(outputgeo, 'a+') as outPgeo:
                outPgeo.write(']}')
            outPgeo.close()
        except IncompleteRead: 
            print "Twitter Restriction set in... \nALL THAT BEAUTIFUL DATA :'(\n"
            time.sleep(10) # sleep for 10 seconds twitters restrictions

    else:
        # write last line of old one:
        with open(outputgeo, 'a+') as outPgeo:
            outPgeo.write(']}')
        outPgeo.close()

        # publish old one for one week
        with open(outputgeo, 'r') as uploadFile:
            uploadFileJSON = json.loads(uploadFile)
        uploadFile.close()
        REDIS.setex(outputgeo, uploadFileJSON, 60*60*24*7) # a week in seconds
        # stats_ARRAY_HOUR_DATE -> ((ALL, WITH_GEO), (ALL_INTV, WITH_GEO_INTV))
        REDIS.set("stats_{0}_{1}_{2}".format(searchArray, currentKeyDateTime.split(':')[0], currentKeyDateTime.split(':')[1]), ((counAll, countLoc), (countAll_intervall, countLoc_intervall)))
        countAll_intervall = 0 
        countLoc_intervall = 0 
        
        # Delete old file?
        if DELETE_OLD: os.remove(outputgeo)

        # update KeyDateTime and nowDateTime:
        currentKeyDateTime = getCurrentDateKey()
        nowDateTime = getCurrentDateKey()        
        # set new name:
        outputgeo = outputgeo_tpl % (searchArray, currentKeyDateTime.split(':')[0], currentKeyDateTime.split(':')[1])

        # write first line of new one
        with open(outputgeo, 'a+') as outPgeo:
            outPgeo.write('{"type":"FeatureCollection","features":[')
            outPgeo.write('\n')
        outPgeo.close()
        # Now back to main loop




