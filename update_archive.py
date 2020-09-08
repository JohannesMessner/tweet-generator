import json
import tweepy
import numpy as np
import pandas as pd


def authenticate():
    # a file named credentials.json must contain twitter-developers/api credentials in order to access online tweets
    with open('credentials.json') as f:
        credentials = json.load(f)
        auth = tweepy.OAuthHandler(credentials['api_key'], credentials['api_secret'])
        auth.set_access_token(credentials['access_token'], credentials['access_token_secret'])
        return tweepy.API(auth)


def get_new_tweets(user_id, api):
    clean_tweets = set()
    for status in tweepy.Cursor(api.user_timeline, id=user_id, count=3000, tweet_mode='extended').items():
        tweet = status.full_text
        # disregard retweets
        if tweet.startswith('RT'):
            continue
        else:
            clean_tweets.add(tweet)
    return clean_tweets


def get_archive_tweets(archive_filename):
    tweets = pd.read_csv(archive_filename).to_numpy().tolist()
    tweets = list(map(lambda x: x[1], tweets))
    return set(tweets)


def update_archive(user_id='realDonaldTrump'):
    api = authenticate()

    # get tweets from users timeline
    latest_tweets = get_new_tweets(user_id, api)
    # tweets that are already stored locally
    filename = user_id + '.csv'
    archive_tweets = get_archive_tweets(filename)
    # union of both sets
    tweets = pd.DataFrame(list(set.union(latest_tweets, archive_tweets)))
    # write back updated set
    tweets.to_csv(filename)


def main():
    update_archive()


if __name__ == '__main__':
    main()