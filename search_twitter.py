from vaderSentiment.vaderSentiment import sentiment as vaderSentiment
from TwitterSearch import *
import csv
import json
import pandas as pd
from openpyxl import load_workbook
import datetime
from helper_functions import write_to_excel

input_file = 'search_terms.txt'
database_file = 'tweets_final.xlsx'
geolocator = Nominatim()

print(datetime.datetime.now())

ts = TwitterSearch(
    consumer_key = 'XewW4OX5LAGQzgTEAmQGlkTzS',
    consumer_secret = 'wMitBoHSRF9MNCU4KK5ROUTMMvHzwT2UKMR7xmXqCEr8UYqRap',
    access_token = '36265587-LrXamUdtqL90PByCFLrZdj0CKniW6AMYayIkUoxiR',
    access_token_secret = '5aWqMLTEYLRuDcE8OTV30MNSMsNmF4rMvy4qlQjbS33jK'
)

df = pd.DataFrame([], columns=["keyword", "username", "text", "lat", "lng", "location", "created_at", "place", "description", "verified", "sentiment_score", "compound_sentiment", "description_sentiment"])

def run_twitter_search(keyword, output_file):
    print(keyword.upper())
    counter = 0
    try:
        tso = TwitterSearchOrder() # create a TwitterSearchOrder object
        tso.set_keywords([str(keyword)]) # let's define all words we would like to have a look for
        # tso.set_language('en') # we want to see English tweets only
        tso.set_include_entities(True) # and don't give us all those entity information
        tso.set_geocode(45.551279, -92.586955, 530, imperial_metric=True)

        for tweet in ts.search_tweets_iterable(tso):
            counter = counter + 1
            search_term = keyword
            username = "NONE" if tweet['user']['screen_name'] is None else tweet['user']['screen_name']
            text = "NONE" if tweet['text'] is None else tweet['text']
            place = "NONE" if tweet['place'] is None else tweet['place']
            if (tweet['coordinates'] is not None):
                lat = tweet['coordinates']['coordinates'][1]
                lng = tweet['coordinates']['coordinates'][0]
            elif (tweet['place'] is not None):
                place_coordinates = tweet['place']['bounding_box']['coordinates']
                sum_lat = 0
                sum_lng = 0
                for pair in place_coordinates[0]:
                    sum_lat += pair[1]
                    sum_lng += pair[0]
                lat = sum_lat / len(place_coordinates[0])
                lng = sum_lng / len(place_coordinates[0])
                place = tweet['place']['full_name']
            else:
                lat = "NONE"
                lng = "NONE"
            location = "NONE" if tweet['user']['location'] is None else tweet['user']['location']
            created_at = "NONE" if tweet['created_at'] is None else tweet['created_at']
            description = "NONE" if tweet['user']['description'] is None else tweet['user']['description']
            verified = "NONE" if tweet['user']['verified'] is None else str(tweet['user']['verified'])
            sentiment_score = vaderSentiment(text.encode('utf-8'))
            compound_sentiment = sentiment_score['compound']
            description_sentiment = vaderSentiment(description.encode('utf-8'))['compound']
            try:
                df.loc[len(df)] = [search_term, username, text, lat, lng, location, created_at, place, description, verified, sentiment_score, compound_sentiment, description_sentiment]
                if((len(df) % 200) == 0):
                    write_to_excel(output_file, 'Sheet1', df)
                    print("_%s %s tweets/%s total" % (counter, keyword.upper(), len(df)))
            except:
                write_to_excel(output_file, str(keyword), df)
            if(counter == 10000):
                return
        write_to_excel(output_file, str(keyword), df)
        print("_______%s tweets saved" % (len(df)))

    except TwitterSearchException as e: # take care of all those ugly errors if there are some
        print(e)

search_terms = open(input_file, 'r')
for row in search_terms:
    key_words = row
    run_twitter_search(key_words, database_file)