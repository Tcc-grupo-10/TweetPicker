import urllib
import hashlib
import datetime
from random import randint
from Process import TweetPicker, SpamFiltering, PreProcessing, SentimentClassifier
from Services import TwitterIntegration

# SearchHotkeys
rawKey = "WinterIsHere"

if " " not in rawKey:
    if not rawKey.startswith("#"):
        rawKey = "#" + rawKey

searchEncoded = urllib.quote(rawKey)

rawId = rawKey + "|" + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "|{}".format(randint(0, 100))
runId = hashlib.md5(rawId.encode()).hexdigest()

# Getting token "userless"
tokenUserless = TwitterIntegration.getTokenUserless()

# Get and Process Tweets
numberOfTweets = 50
allTweets = TweetPicker.getTweets(tokenUserless, rawKey, numberOfTweets, searchEncoded, runId)

allTweets = PreProcessing.run(allTweets)

allTweets = SpamFiltering.run(allTweets)

sentiments = SentimentClassifier.run(allTweets)

# TODO -> How we should display this? (Current: JSON)
print (sentiments)
