import urllib
import TwitterIntegration
import TwitterTimelineIterator

#SearchHotkeys
rawKey = "game of thrones"
searchEncoded = urllib.quote(rawKey)

#Getting token "userless"
tokenUserless = TwitterIntegration.getTokenUserless()

#First Search Request
searchRaw = TwitterIntegration.getSearch(searchEncoded, tokenUserless)

#Save tweets and get the new url
nextUrl = TwitterTimelineIterator.saveNext(searchRaw, rawKey)

#Running 15 times
for x in range(0, 15):
    if nextUrl != "":
        searchRaw = TwitterIntegration.getNextSearch(nextUrl, tokenUserless)
        nextUrl = TwitterTimelineIterator.saveNext(searchRaw, rawKey)

