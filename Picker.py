import base64
import urllib2
import urllib
import json

#Twitter's keys
consumerKey = "9cuNRRcqj3wnd7jrUw7Rw1DKw"
consumerSecret = "KZ66L3zmIxQdW0LSwcCoyAN0iXCzusnQTGDmEz6vwAGhq4cFss"

#Twitter's API Token
base64Secret = "Basic " + base64.b64encode(consumerKey+":"+consumerSecret)

#Getting a usable token "userless"
url = 'https://api.twitter.com/oauth2/token'
data = urllib.urlencode({'grant_type': 'client_credentials'})
req = urllib2.Request(url, data)
req.add_header('Authorization', base64Secret)
response = urllib2.urlopen(req).read()
jsonObj = json.loads(response)
bearerToken = jsonObj.get("access_token", "none")



