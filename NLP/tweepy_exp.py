#!/usr/bin/python
# -*- coding: utf-8 -*-

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json
import re
import sys
from tweet2geoJSON import format2geoJSON

from API_KEYS import consumer_key, consumer_secret, access_token, access_token_secret

CUTOFF = -1

countAll = 0
countLoc = 0

outputfile = "tweetsQuake.txt"
outputgeo = "tweetsQuake.geojson"

with open(outputgeo, 'a+') as outPgeo:
    outPgeo.write("{'type':'FeatureCollection','features':[")
    outPgeo.write('\n')
outPgeo.close()

class StdOutListener(StreamListener):

    def on_data(self, data):
        global countLoc, countAll
        
        tweet = json.loads(data)

        if countLoc == CUTOFF : exit(0)

        # only show english & german tweets with geo location and or place defined: TODO
        if (("coordinates" in tweet) or ("place" in tweet)): # and ("lang" in tweet["user"]) and (tweet["user"]["lang"] == "en" or tweet["user"]["lang"] == "de"):
            """
            if (tweet["coordinates"] == None):
                print( '@%s tweeted: %s\nPlace: %s\n' % ( tweet['user']['screen_name'], tweet['text'], tweet["place"]) )
            elif (tweet["place"] == None):
                print( '@%s tweeted: %s\nlat, lng: %s\n' % ( tweet['user']['screen_name'], tweet['text'], tweet["coordinates"] ) )
            else:
                print( '@%s tweeted: %s\nPlace, lat, lng: %s, %s\n' % ( tweet['user']['screen_name'], tweet['text'], tweet["place"], tweet["coordinates"]) )
            """
        print('@%s tweeted: %s\nPlace: %s (%s)\n' % ( tweet['user']['screen_name'], tweet['text'], tweet['place'], tweet['coordinates']))
        countAll += 1

        # write to .txt file
        with open(outputfile, 'a+') as outP:
                outP.write(str(tweet)) 
                outP.write('\n')
        outP.close()
        # convert to and write as .geoJSON:
        geoJson = (str(format2geoJSON(tweet)))
        if geoJson != "":
            with open(outputgeo, 'a+') as outPgeo:
                outPgeo.write(geoJson)
                outPgeo.write('\n')
            outPgeo.close()
            countLoc += 1

        if countAll%100 == 0:
            print "Saw {0} tweets; {1} of them had location information!\n".format(countAll, countLoc)

        return True

    def on_error(self, status):
        print 'Error: ', status

if __name__ == '__main__':
    try:
        l = StdOutListener()
        auth = OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)

        stream = Stream(auth, l)

        if len(sys.argv) < 2 : 
    	   print 'USAGE : python get_tweets.py [n: CUTOFF] [keyword1 keyword2 ... keywordn]'
    	   exit(0)

        try : 
            CUTOFF = int(sys.argv[1])
            queries = sys.argv[2:]
        except : queries = sys.argv[1:]

        stream.filter(track=queries)

    except KeyboardInterrupt:
        print "\n\nYOU INTERRUPTED!\nFINISH WRITING FILE\n"
        print "Saw {0} tweets; {1} of them had location information!\n".format(countAll, countLoc)
        with open(outputgeo, 'a+') as outPgeo:
            outPgeo.write("]}")
        outPgeo.close()

