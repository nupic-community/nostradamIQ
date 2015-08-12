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

outputfile = "tweets.txt"
outputgeo = "tweets.geojson"

class StdOutListener(StreamListener):

    count = 0

    def on_data(self, data):
        tweet = json.loads(data)

        if self.count == CUTOFF : exit(0)

        # only show english & german tweets with geo location and or place defined: TODO
        """
        if ("lang" in tweet["user"]) and (tweet["user"]["lang"] == "en" or tweet["user"]["lang"] == "de") and ("geo" in tweet or "place" in tweet):
            if (not "geo" in tweet.keys()):
                print( '@%s tweeted: %s\nPlace: %s\n' % ( tweet['user']['screen_name'], tweet['text'], tweet["place"]) )
            elif (not "place" in tweet.keys()):
                print( '@%s tweeted: %s\nlat, lng: %s\n' % ( tweet['user']['screen_name'], tweet['text'], tweet["geo"][0], tweet["geo"][1] ) )
            else:
                print( '@%s tweeted: %s\nPlace, lat, lng: %s, %s\n' % ( tweet['user']['screen_name'], tweet['text'], tweet["place"], tweet["geo"][0], tweet["geo"][1] ) )
        """
        print('@%s tweeted: %s\nPlace: %s (%s)\n' % ( tweet['user']['screen_name'], tweet['text'], tweet['place'], tweet['geo']))
        self.count += 1

        # write to .txt file
        with open(outputfile, 'a+') as outP:
                outP.write(str(tweet)) 
                outP.write('\n')
        outP.close()
        # convert and write as geoJSON:
        with open(outputgeo, 'a+') as outPgeo:
            outPgeo.write(str(format2geoJSON(tweet)))
            outPgeo.write('\n')
        outPgeo.close()

        return True

    def on_error(self, status):
        print 'Error: ', status

if __name__ == '__main__':
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
