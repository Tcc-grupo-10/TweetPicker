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


#TODO - Set a timmer of 15 minutes and run the "for" again
#TODO - Check if we just can call the search 15 times or is 180
#TODO - Change the count of TwitterIntegration to 100 - (1 - to Test)
#TODO - Change DynamoDB from Local to the Cloud (using env vars)
#TODO - Write the README
#TODO - If we have time, change to Python 3 (current 2.7)
#TODO - If we have time, use "user token" - browser needed