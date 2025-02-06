# Xに投稿するプログラム

# Twitter APIライブラリをインポートする
import tweepy
import os

# Twitter APIキーを環境変数から取得
consumerKey = os.environ["TWITTER_CONSUMER_KEY"]       # API Key
consumerSecret = os.environ["TWITTER_CONSUMER_SECRET"] # API Key Secret
accessToken = os.environ["TWITTER_ACCESS_TOKEN"]
accessTokenSecret = os.environ["TWITTER_ACCESS_TOKEN_SECRET"]
bearerToken = os.environ["TWITTER_BEARER_TOKEN"]

# Xに投稿する関数を定義
def post(tweet):
    #tweepy クライアントを作成
    client = tweepy.Client(
        bearerToken,
        consumerKey,
        consumerSecret,
        accessToken,
        accessTokenSecret
    )

    # Tweetを投稿
    client.create_tweet(text=tweet)