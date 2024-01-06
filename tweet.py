import gpt_twitter
import bot_twitter

tweet = gpt_twitter.make_tweet()
bot_twitter.post(tweet)