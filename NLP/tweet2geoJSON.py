"""
SCHEME:

{
  "type": "Feature",
  "geometry": {
    "type": "Point",
    "coordinates": [-122.09,37.64 ]
  },
  "properties": {
    "name": "@BrianLehman",
    "tweet_body": "I freaking love maps!",
  }
}
"""

def place_lookup(place):
	#TODO 

	return [lat, lng]

def format2geoJSON(tweet):
	if tweet["geo"] != 'null':
		# get lat,lng and create geoJSON object:
		tweet_geoJSON = {
						  "type": "Feature",
						  "geometry": {
						    "type": "Point",
						    "coordinates": tweet['geo'], #[lat,lng]
						    "img": tweet['user']["profile_image_url"]
						  },
						  "properties": {
						    "name": tweet['user']['screen_name'],
						    "user_description": tweet['user']['description'],
						    "place": tweet["place"],
						    "user__has_extended_profile": tweet['user']["has_extended_profile"],
						    "followers_count": tweet['user']['followers_count'],
						    "verified": tweet['user']['verified'],
						    "lang": tweet['user']['lang'],
						    "tweet_body": tweet['text'],
						    "time": tweet['created_at'],
						    "favorite_count": tweet["favorite_count"],
						    "retweeted": tweet['retweeted'],
						    "in_reply_to_user_id_str": tweet["in_reply_to_user_id_str"],
						    "in_reply_to_status_id_str": tweet["in_reply_to_status_id_str"],
						    "possibly_sensitive": tweet["possibly_sensitive"],
						    "hashtags": tweet["entities"]["hashtags"],
						    "symbols": tweet["entities"]["symbols"],
						    "user_mentions": tweet["entities"]["user_mentions"],
						    "urls": tweet["entities"]["urls"],
						  }
						}

		return tweet_geoJSON


	elif tweet["place"] != 'null':
		# convert place to lat,lng and create geoJSON object:
		coords = place_lookup(tweet["place"])
		tweet_geoJSON = {
						  "type": "Feature",
						  "geometry": {
						    "type": "Point",
						    "coordinates": coords
						    "img": tweet['user']["profile_image_url"]
						  },
						  "properties": {
						    "name": tweet['user']['screen_name'],
						    "user_description": tweet['user']['description'],
						    "place": tweet["place"],
						    "user__has_extended_profile": tweet['user']["has_extended_profile"],
						    "followers_count": tweet['user']['followers_count'],
						    "verified": tweet['user']['verified'],
						    "lang": tweet['user']['lang'],
						    "tweet_body": tweet['text'],
						    "time": tweet['created_at'],
						    "favorite_count": tweet["favorite_count"],
						    "retweeted": tweet['retweeted'],
						    "in_reply_to_user_id_str": tweet["in_reply_to_user_id_str"],
						    "in_reply_to_status_id_str": tweet["in_reply_to_status_id_str"],
						    "possibly_sensitive": tweet["possibly_sensitive"],
						    "hashtags": tweet["entities"]["hashtags"],
						    "symbols": tweet["entities"]["symbols"],
						    "user_mentions": tweet["entities"]["user_mentions"],
						    "urls": tweet["entities"]["urls"],
						  }
						}
		return tweet_geoJSON


	else: return ""
