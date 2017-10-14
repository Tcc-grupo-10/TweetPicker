import urllib
import hashlib
import datetime
from random import randint
from Process import TweetPicker
from Services import TwitterIntegration
from Process import PreProcessing

# SearchHotkeys
rawKey = "WinterIsHere"

if not rawKey.startswith("#"):
    rawKey = "#" + rawKey
searchEncoded = urllib.quote(rawKey)

rawId = rawKey + "|" + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "|{}".format(randint(0, 100))
runId = hashlib.md5(rawId.encode()).hexdigest()

# Getting token "userless"
tokenUserless = TwitterIntegration.getTokenUserless()

# Get and Process Tweets
numberOfTweets = 50
gotThemAll = TweetPicker.getTweets(tokenUserless, rawKey, numberOfTweets, searchEncoded, runId)
# TODO -> Wait this get done (check if the return True worked)

PreProcessing.run()

