import base64
import urllib
import urllib.request
import json
import os

#Twitter's keys

consumerKeyTwitter = os.environ['consumer_key_twitter']
consumerSecretTwitter = os.environ['consumer_secret_twitter']

#Twitter's API Token
base64Secret = "Basic " + base64.b64encode(consumerKeyTwitter+":"+consumerSecretTwitter)


def getTokenUserless():
    url = 'https://api.twitter.com/oauth2/token'
    data = urllib.urlencode({'grant_type': 'client_credentials'})
    req = urllib.Request(url, data)
    req.add_header('Authorization', base64Secret)
    response = urllib.urlopen(req).read()
    jsonObj = json.loads(response)
    return "Bearer " + jsonObj.get("access_token", "none")


def getSearch(searchEncoded, bearerToken):
    url = 'https://api.twitter.com/1.1/search/tweets.json?q='+searchEncoded+"&lang=en&count=100"
    req = urllib.Request(url)
    req.add_header('Authorization', bearerToken)
    response = urllib.urlopen(req).read()
    jsonO = json.loads(response)
    #print(json.dumps(jsonO, indent=4))
    return jsonO

def getNextSearch(nextUrl, bearerToken):
    url = 'https://api.twitter.com/1.1/search/tweets.json'+nextUrl
    print (url)
    req = urllib.Request(url)
    req.add_header('Authorization', bearerToken)
    response = urllib.urlopen(req).read()
    jsonO = json.loads(response)
    #print(json.dumps(jsonO, indent=4))
    return jsonO