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

http://geojson.org/geojson-spec.html#bounding-boxes

""" 
from getLocation import get_coordinates

def check_text_for_location(text):
	# Search the tweet for possible geolocations by checkin if google knows the string:
	coords_array = [] # What to do when we find multiple?
	for #TODO
		query = None 
		coords = get_coordinates(query) # Returns [lat, lng] or None if not found
		if coords != None:
			# return coords if we find sth:
			# return coords
			coords_array.append(coords)
			
	# otherwise return None if you don't find anything
	return None


def place_lookup(tweet):
	# https://twittercommunity.com/t/schema-of-boundingbox-in-places-section/8663
	boundingBox = tweet["place"]["bounding_box"]["coordinates"][0]
	lat = float((boundingBox[0][0] + boundingBox[1][0]) / 2.0)
	lng = float((boundingBox[1][1] + boundingBox[2][1]) / 2.0)
	return [lat, lng]

def format2geoJSON(tweet):
	# check for all possibilities:
	# 1: tweet contains Coord info AND tweets about another loation
	# 2. tweet contains coord info and no location in the body
	# 3. tweet contains place info AND location in body
	# 4. tweet contains place and no location in the body
	# 5. tweet contains no location info, but tweets about another place
	# 6. tweet is useless; no location info at all
	try:
		if tweet["coordinates"] != None: # Twitter already did the job!
			# get lat,lng and create geoJSON object:
			coords_in_tweet = check_text_for_location(tweet["text"])
			if coords_in_tweet == None: # (2) Nothing found in the text, use only the coords
				tweet_geoJSON = {
								  "type": "Feature",
								  "geometry": {
								    "type": "Point",
								    "coordinates": tweet["coordinates"]
								  },
								  "properties": {
								    "name": tweet["user"]["screen_name"],
								    "user_description": tweet["user"]["description"],
								    "user_img": tweet["user"]["profile_image_url"],
								    "place": tweet["place"],
								    "default_profile": tweet["user"]["default_profile"],
								    "followers_count": tweet["user"]["followers_count"],
								    "verified": tweet["user"]["verified"],
								    "lang": tweet["user"]["lang"],
								    "tweet_body": tweet["text"],
								    "time": tweet["created_at"],
								    "favorite_count": tweet["favorite_count"],
								    "retweeted": tweet["retweeted"],
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
			else: # tweets about another location (1)
				# Build a line between the two coords:
				tweet_line_geoJSON = {
									  "type": "Feature",
									  "geometry": {
									    "type": "LineString",
									    "coordinates": [coords, coords_in_tweet]
									  },
									  "style":{
										        "fill": "blue"
									  },
									  "properties": {
									    "name": tweet["user"]["screen_name"],
									    "user_description": tweet["user"]["description"],
									    "user_img": tweet["user"]["profile_image_url"],
									    "place": tweet["place"],
									    "default_profile": tweet["user"]["default_profile"],
									    "followers_count": tweet["user"]["followers_count"],
									    "verified": tweet["user"]["verified"],
									    "lang": tweet["user"]["lang"],
									    "tweet_body": tweet["text"],
									    "time": tweet["created_at"],
									    "favorite_count": tweet["favorite_count"],
									    "retweeted": tweet["retweeted"],
									    "in_reply_to_user_id_str": tweet["in_reply_to_user_id_str"],
									    "in_reply_to_status_id_str": tweet["in_reply_to_status_id_str"],
									    "possibly_sensitive": tweet["possibly_sensitive"],
									    "hashtags": tweet["entities"]["hashtags"],
									    "symbols": tweet["entities"]["symbols"],
									    "user_mentions": tweet["entities"]["user_mentions"],
									    "urls": tweet["entities"]["urls"],
									  }
									}
				}
				return tweet_line_geoJSON

		elif tweet["place"] != None: # Find the associated Place
			# convert place to lat,lng and create geoJSON object:
			coords = place_lookup(tweet)
			coords_in_tweet = check_text_for_location(tweet["text"])
			if coords_in_tweet == None: # (4)
				tweet_geoJSON = {
								  "type": "Feature",
								  "geometry": {
								    "type": "Point",
								    "coordinates": coords
								  },
								  "properties": {
								    "name": tweet["user"]["screen_name"],
								    "user_description": tweet["user"]["description"],
								    "user_img": tweet["user"]["profile_image_url"],
								    "place": tweet["place"],
								    "default_profile": tweet["user"]["default_profile"],
								    "followers_count": tweet["user"]["followers_count"],
								    "verified": tweet["user"]["verified"],
								    "lang": tweet["user"]["lang"],
								    "tweet_body": tweet["text"],
								    "time": tweet["created_at"],
								    "favorite_count": tweet["favorite_count"],
								    "retweeted": tweet["retweeted"],
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
			else: # (3)
				# Build a line between the two coords:
				tweet_line_geoJSON = {
									  "type": "Feature",
									  "geometry": {
									    "type": "LineString",
									    "coordinates": [coords, coords_in_tweet]
									  },
									  "style":{
										        "fill": "blue"
									  },
									  "properties": {
									    "name": tweet["user"]["screen_name"],
									    "user_description": tweet["user"]["description"],
									    "user_img": tweet["user"]["profile_image_url"],
									    "place": tweet["place"],
									    "default_profile": tweet["user"]["default_profile"],
									    "followers_count": tweet["user"]["followers_count"],
									    "verified": tweet["user"]["verified"],
									    "lang": tweet["user"]["lang"],
									    "tweet_body": tweet["text"],
									    "time": tweet["created_at"],
									    "favorite_count": tweet["favorite_count"],
									    "retweeted": tweet["retweeted"],
									    "in_reply_to_user_id_str": tweet["in_reply_to_user_id_str"],
									    "in_reply_to_status_id_str": tweet["in_reply_to_status_id_str"],
									    "possibly_sensitive": tweet["possibly_sensitive"],
									    "hashtags": tweet["entities"]["hashtags"],
									    "symbols": tweet["entities"]["symbols"],
									    "user_mentions": tweet["entities"]["user_mentions"],
									    "urls": tweet["entities"]["urls"],
									  }
									}
				}
				return tweet_line_geoJSON


		else: # Twitter finds no geoLoc:
			coords = check_text_for_location(tweet["text"])
			if coords == None: # (6)
				return None
			else: # (5)
				tweet_geoJSON = {
							  "type": "Feature",
							  "geometry": {
							    "type": "Point",
							    "coordinates": coords
							  },
							  "properties": {
							    "name": tweet["user"]["screen_name"],
							    "user_description": tweet["user"]["description"],
							    "user_img": tweet["user"]["profile_image_url"],
							    "place": tweet["place"],
							    "default_profile": tweet["user"]["default_profile"],
							    "followers_count": tweet["user"]["followers_count"],
							    "verified": tweet["user"]["verified"],
							    "lang": tweet["user"]["lang"],
							    "tweet_body": tweet["text"],
							    "time": tweet["created_at"],
							    "favorite_count": tweet["favorite_count"],
							    "retweeted": tweet["retweeted"],
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
	# Don't fail on errors
	except: return None 

