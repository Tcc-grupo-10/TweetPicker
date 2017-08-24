import urllib
import TwitterIntegration

#SearchHotkeys
rawKey = "game of thrones"
searchEncoded = urllib.quote(rawKey)

tokenUserless = TwitterIntegration.getTokenUserless()
searchRaw = TwitterIntegration.getSearch(searchEncoded, tokenUserless)
