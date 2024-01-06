import tweepy
import os

# 環境変数からTwiiter APIキーを取得する
consumerKey = os.environ["TWITTER_CONSUMER_KEY"]
consumerSecret = os.environ["TWITTER_CONSUMER_SECRET"]
accessToken = os.environ["TWITTER_ACCESS_TOKEN"]
accessTokenSecret = os.environ["TWITTER_ACCESS_TOKEN_SECRET"]
bearerToken = os.environ["TWITTER_BEARER_TOKEN"]

# ツイート作成関数
def post(tweet):

    client = tweepy.Client(
        bearerToken,
        consumerKey,
        consumerSecret,
        accessToken,
        accessTokenSecret
    )

    client.create_tweet(text=tweet)