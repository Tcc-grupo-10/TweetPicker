import base64
import urllib
import urllib2
import json

#Twitter's keys
consumerKeyTwitter = "9cuNRRcqj3wnd7jrUw7Rw1DKw"
consumerSecretTwitter = "KZ66L3zmIxQdW0LSwcCoyAN0iXCzusnQTGDmEz6vwAGhq4cFss"

#Twitter's API Token
base64Secret = "Basic " + base64.b64encode(consumerKeyTwitter+":"+consumerSecretTwitter)


def getTokenUserless():
    url = 'https://api.twitter.com/oauth2/token'
    data = urllib.urlencode({'grant_type': 'client_credentials'})
    req = urllib2.Request(url, data)
    req.add_header('Authorization', base64Secret)
    response = urllib2.urlopen(req).read()
    jsonObj = json.loads(response)
    return "Bearer " + jsonObj.get("access_token", "none")


def getSearch(searchEncoded, bearerToken):
    url = 'https://api.twitter.com/1.1/search/tweets.json?q='+searchEncoded+"&lang=en&count=1"
    req = urllib2.Request(url)
    req.add_header('Authorization', bearerToken)
    response = urllib2.urlopen(req).read()
    jsonO = json.loads(response)
    #print(json.dumps(jsonO, indent=4))
    return jsonO

def getNextSearch(nextUrl, bearerToken):
    url = 'https://api.twitter.com/1.1/search/tweets.json'+nextUrl
    print url
    req = urllib2.Request(url)
    req.add_header('Authorization', bearerToken)
    response = urllib2.urlopen(req).read()
    jsonO = json.loads(response)
    print "HEUHEUEHUEHEU"
    print(json.dumps(jsonO, indent=4))
    return jsonO