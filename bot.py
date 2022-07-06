'''

Author: Curtiss Williams
Description: Tweets a random quote from the Fallout: New Vegas base game
once every hour.

'''
import firebase_admin
from firebase_admin import db
from firebase_admin import credentials
import tweepy
import config
import random
import time

def main():
    cred = credentials.Certificate("service-file.json")
    firebase_admin.initialize_app(cred, {"databaseURL":"databaseURL"})
    
    client = tweepy.Client(
        consumer_key=config.consumer_key,
        consumer_secret=config.consumer_secret,
        access_token=config.access_token,
        access_token_secret=config.access_secret,
    )
    
    ref = db.reference("/")
    keys = list(ref.get(shallow=True))

    INTERVAL = 3600
    quotes = []
    while True:
        if len(quotes) == 0:
            for _ in range(24): # get array of tweets for the day
                key = random.choice(keys)
                quotes.append(random.choice(db.reference(key).get()))
        quote = quotes.pop()
        client.create_tweet(text=quote)
        time.sleep(INTERVAL)

if __name__ == '__main__':
    main()
