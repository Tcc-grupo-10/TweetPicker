import urllib
import TwitterIntegration
import TwitterTimelineIterator

#SearchHotkeys
rawKey = "game of thrones"
searchEncoded = urllib.quote(rawKey)

#Getting token "userless"
tokenUserless = TwitterIntegration.getTokenUserless()

#Get and Process Tweets
TwitterTimelineIterator.getTweetsRec(tokenUserless, rawKey, "", 449, 1, searchEncoded)

#TODO - If we have time, change to Python 3 (current 2.7)
#TODO - If we have time, use "user token" - browser needed