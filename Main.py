import urllib

import TwitterIntegration
from Process import TweetPicker

# SearchHotkeys
rawKey = "WinterIsHere"

if not rawKey.startswith("#"):
    rawKey = "#" + rawKey
searchEncoded = urllib.quote(rawKey)

# TODO -> CREATE A RUN_ID

# Getting token "userless"
tokenUserless = TwitterIntegration.getTokenUserless()

# Get and Process Tweets
# TODO -> Get a fixed number of tweets.. not a infinity loop
TweetPicker.getTweetsRec(tokenUserless, rawKey, "", 449, 1, searchEncoded)
# TODO -> Wait this get done



