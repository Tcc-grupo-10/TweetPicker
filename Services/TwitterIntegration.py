import base64
import urllib
import urllib.parse

import json
from urllib.request import Request, urlopen
import os

#Twitter's keys

consumerKeyTwitter = "m7zD4lOJNCLB7Ohvw7I3pbFDv"
consumerSecretTwitter = "deMEHMgSQ7nlOigSc6WfSd081K5NeAi3Denw5knsGEpGUvshLv"
#Twitter's API Token
base64Secret = "Basic {}".format(base64.b64encode((consumerKeyTwitter+":"+consumerSecretTwitter).encode('utf-8'))).replace("b'", "")

def getTokenUserless():
    url = 'https://api.twitter.com/oauth2/token'
    data = urllib.parse.urlencode({'grant_type': 'client_credentials'}).encode('utf-8')

    req = urllib.request.Request(
        url,
        data=data,
        headers={
            'Authorization': base64Secret
        }
    )

    f = urllib.request.urlopen(req)
    response = f.read()
    jsonObj = json.loads(response)
    return "Bearer {}".format(jsonObj.get("access_token", "none"))

def getSearch(searchEncoded, bearerToken):
    url = 'https://api.twitter.com/1.1/search/tweets.json?q='+searchEncoded+"&lang=en&count=100"
    req = urllib.request.Request(url)
    req.add_header('Authorization', bearerToken)
    response = urlopen(req).read()
    jsonO = json.loads(response)
    #print(json.dumps(jsonO, indent=4))
    return jsonO

def getNextSearch(nextUrl, bearerToken):
    url = 'https://api.twitter.com/1.1/search/tweets.json'+nextUrl
    print ((url))
    req = urllib.request.Request(url)
    req.add_header('Authorization', bearerToken)
    response = urllib.request.urlopen(req).read()
    jsonO = json.loads(response)
    #print(json.dumps(jsonO, indent=4))
    return jsonO