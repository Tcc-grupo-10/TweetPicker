import urllib
import TwitterIntegration
import TwitterTimelineIterator

# SearchHotkeys
rawKey = "WinterIsHere"

if not rawKey.startswith("#"):
    rawKey = "#" + rawKey
searchEncoded = urllib.quote(rawKey)

# TODO -> Drop the last run with the same #? Use the same results?

# Getting token "userless"
tokenUserless = TwitterIntegration.getTokenUserless()

# Get and Process Tweets
# TODO -> Get a fixed number of tweets.. not a infinity loop
TwitterTimelineIterator.getTweetsRec(tokenUserless, rawKey, "", 449, 1, searchEncoded)


