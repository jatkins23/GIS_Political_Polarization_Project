import geocoder
import pandas as pd
import json
import csv
import datetime
from helper_functions import write_to_excel
import os

GOOGLE_API_KEY = os.environ['GOOGLE_API_KEY']

input_file = 'tweets_final_removed.xlsx'
output_file = 'geocoded_tweets_final.xlsx'

df_output = pd.DataFrame([], columns=["keyword", "username", "text", "lat", "lng", "location", "created_at", "place", "description", "verified", "sentiment_score", "compound_sentiment", "description_sentiment"])
print('Adding sheets')

try:
    df_input = df_input.append(pd.read_excel(input_file, 'Sheet1'))
    print('Sheet1 added')
except:
    print("error adding Sheet1")
try:
    df_input = pd.read_excel(input_file, 'Sheet2')
    print('Sheet2 added')
except:
    print("error adding Sheet2")
try:
    df_input = pd.read_excel(input_file, 'Sheet3')
    print('Sheet3 added')
except:
    print("error adding Sheet3")
try:
    df_input = df_input.append(pd.read_excel(input_file, 'Sheet4'))
    print('Sheet4 added')
except:
    print("error adding Sheet4")
try:
    df_input = df_input.append(pd.read_excel(input_file, 'Sheet5'))
    print('Sheet5 added')
except:
    print("error adding Sheet5")

print len(df_input)

counter = 0
dns_counter = 0
num_left = len(df_input)
for index, tweet in df_input.iterrows():
    num_left -= 1
    if((tweet.lat == 0 and tweet.lng == 0) or (tweet.lat == 'NONE' or tweet.lng == 'NONE')):
        if (not pd.isnull(tweet.location)):
            if "DO_NOT_SEARCH" in tweet.location:
                print("DO_NOT_SEARCH here")
                dns_counter += 1
            else:
                googleLocation = geocoder.google(tweet.location, key=GOOGLE_API_KEY)
                coordinates = googleLocation.latlng
                if (len(coordinates) == 2):
                    # warning: unless any of the input data has decimal values in it, this will auto-round the coordinates
                    newLat = coordinates[0]
                    newLng = coordinates[1]
                    counter += 1
                    df_output.loc[len(df_output)] = [tweet.keyword, tweet.username, tweet.text, newLat, newLng, tweet.location, tweet.created_at, tweet.place, tweet.description, tweet.verified, tweet.sentiment_score, tweet.compound_sentiment, tweet.description_sentiment]
                    print("stored: %s, to go: %s, dns: %s" % (counter, num_left, dns_counter))

                    if((counter % 200) == 0):
                        try:
                            write_to_excel(output_file, 'Sheet1', df_output)
                            print("%s SAVED" % (counter))
                        except:
                            print("ERROR saving new coordinates")
                            # return
                else:
                    print("coordinates not found for '%s' - dropping tweet by %s" % (tweet.location, tweet.username))   
        else:
            print("no location information - dropping tweet by %s" % (tweet.username))
    else:
        counter += 1
        print("coordinates already found")
        df_output.loc[len(df_output)] = [tweet.keyword, tweet.username, tweet.text, tweet.lat, tweet.lng, tweet.location, tweet.created_at, tweet.place, tweet.description, tweet.verified, tweet.sentiment_score, tweet.compound_sentiment, tweet.description_sentiment]
        print("stored: %s, to go: %s, dns: %s" % (counter, num_left, dns_counter))
        
        if((counter % 200) == 0):
            try:
                write_to_excel(output_file, 'Sheet1', df_output)
                print("%s SAVED" % (counter))
            except:
                print("ERROR saving old coordinates")



write_to_excel(output_file, 'Sheet1', df_output)
print("final results: %s/%s saved" % (counter, len(df_input)))
