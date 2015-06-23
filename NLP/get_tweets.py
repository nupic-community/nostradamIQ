#! /usr/bin/env python 

from TwitterSearch import *
import time
import requests

# see: https://dev.twitter.com/rest/reference/get/search/tweets
# BASE_URL = "https://api.twitter.com/1.1/search/tweets.json"
# and https://github.com/ckoepp/TwitterSearch

from API_KEYS import consumer_key, consumer_secret, access_token, access_token_secret


# keywords = ["earthquake", "quake"]

keyword_files = ["corpori/animals_unique_translated.txt", "corpori/adjectives_unique_translated.txt", "corpori/earthquakes_unique_translated.txt"]

outputfile = "tweets.txt"


def get_keywords(filename):
        keywords = []
        with open(filename, 'r') as inF:
                for line in inF:
                        keywords.append(line)                        
        inF.close()
        return keywords
        

def test_language(tso, language):
        try:
            # load  currently supported languages by Twitter and store them in a TwitterSearchOrder object
            ts.set_supported_languages(tso)

            # try to set language (see ISO 639-1) 
            ts.set_language(language)
            print('{0} seems to be officially supported by Twitter. Yay!'.format(language))
            return 0

        except TwitterSearchException as e:

            # if we get an 1002 code it means that <language> is not supported (see TwitterSearchException)
            if e.code == 1002:
                print('Oh no - {0} is not supported :('.format(language))
            print(e)
            return 0


def searchTweets(keywordLists=None, language=None, geo_lat=None, geo_lng=None, geo_rad=None, timeStart=None, timeStop=None, no_entities=False, no_retweets=False, no_links=False, no_answers=False):
        tweetsFound = []
        tweetsCount = 0
        tso = TwitterSearchOrder()
        # remove all restrictions from previos calls:
        tso.remove_all_filters()
        # this makes sure no videos/pics are commented
        tso.set_keywords(["-video", "-pic", "-foto", "-funny", "-clip", "-vid", "-movie", "-song"]) # append more synonyms and other languages TODO
        try:
            tso = TwitterSearchOrder() 
            if keywords != None:
                for keywordList in keywordLists:
                        tso.add_keyword(keywordList, or_operator=True)
            if language != None:
                tso.set_language(str(language))
            if geo_rad != None and geo_lat != None and geo_lng != None:
                tso.set_geocode(geo_lat, geo_lng, geo_rad, imperial_metric=True) # must be of format: str(lat,lng,radius) + 'km'/'mi'
            if timeStart != None:
                tso.add_keyword('since:' + str(timeStart)) # time has to be of the format: YYYY-MM-DD
            if timeStop != None:
                tso.add_keyword('until:' + str(timeStop))
            if no_entities:
                tso.set_include_entities(False) 
            if no_retweets:
                pass #tso.set_include_rts(False) TODO
            if no_links:
                pass #TODO
            if no_answers:
                pass #tso.set_exclude_replies(True) TODO
            
            # Maybe use sentiment analysis? // tso.set_negative_attitude_filter()

            ts = TwitterSearch(
                consumer_key = consumer_key,
                consumer_secret = consumer_secret,
                access_token = access_token,
                access_token_secret = access_token_secret)

            for tweet in ts.search_tweets_iterable(tso, callback=my_callback):
                tweetsFound.append(tweet)
                tweetsCount += 1
                with open(outputfile, 'a+') as outP:
                        outP.write(str(tweet)) 
                        outP.write('\n')
                outP.close()
                print( '@%s tweeted: %s' % ( tweet['user']['screen_name'], tweet['text'] ) )

        except TwitterSearchException as e: 
                print(e)
        except requests.exceptions.SSLError as e:
                print(e)
            
        return tweetsFound, tweetsCount
        
               
def my_callback(current_ts_instance): # accepts ONE argument: an instance of TwitterSearch
        queries, tweets_seen = current_ts_instance.get_statistics()
        if queries > 0 and (queries % 10) == 0: # trigger delay every 5th query
                time.sleep(60) # sleep for 60 seconds
            
  
if __name__=='__main__':
        keywordLists = []
        for keyword_file in keyword_files:
                keywordLists.append(get_keywords(keyword_file))
        searchTweets(keywordLists=keywordLists, geo_lat=34.0, geo_lng=-118.0, geo_rad=10, no_retweets=True, no_links=True, no_answers=True)



          
            
