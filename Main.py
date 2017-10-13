import urllib

from Process import TweetPicker
from Services import TwitterIntegration
from Process import PreProcessing

# SearchHotkeys
rawKey = "WinterIsHere"

if not rawKey.startswith("#"):
    rawKey = "#" + rawKey
searchEncoded = urllib.quote(rawKey)

# TODO -> CREATE A VALID RUN_ID ( hash(rawkey + date + random number) ?)
runId = "HEUHEUHUEBRBR"

# Getting token "userless"
tokenUserless = TwitterIntegration.getTokenUserless()

# Get and Process Tweets
numberOfTweets = 50
gotThemAll = TweetPicker.getTweets(tokenUserless, rawKey, numberOfTweets, searchEncoded, runId)
# TODO -> Wait this get done (check if the return True worked)

PreProcessing.run()

