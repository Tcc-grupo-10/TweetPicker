import base64
import urllib
import urllib.request
import urllib.parse
import json
import os

consumerKeyTwitter = os.environ['consumer_key_twitter']
consumerSecretTwitter = os.environ['consumer_secret_twitter']


def getTokenUserless(secret):
    url = 'https://api.twitter.com/oauth2/token'
    data = urllib.parse.urlencode({'grant_type': 'client_credentials'}).encode('utf-8')

    req = urllib.request.Request(
        url,
        data=data,
        headers={
            'Authorization': secret
        }
    )

    f = urllib.request.urlopen(req)
    response = f.read()
    jsonObj = json.loads(response)
    return "Bearer {}".format(jsonObj.get("access_token", "none"))


class TwitterIntegration(object):

    def __init__(self):
        self.secretToken = getTokenUserless("Basic {}".format(base64.b64encode((consumerKeyTwitter+":"+consumerSecretTwitter).encode('utf-8'))).replace("b'", ""))

    def getSearch(self, searchEncoded, count):
        url = 'https://api.twitter.com/1.1/search/tweets.json?q='+searchEncoded+"&lang=en&count={}".format(count)

        req = urllib.request.Request(
            url,
            data=None,
            headers={
                'Authorization': self.secretToken
            }
        )
        f = urllib.request.urlopen(req)
        response = f.read()
        jsonO = json.loads(response)
        #print(json.dumps(jsonO, indent=4))
        return jsonO

    def getNextSearch(self, nextUrl):
        url = 'https://api.twitter.com/1.1/search/tweets.json'+nextUrl
        req = urllib.request.Request(
            url,
            data=None,
            headers={
                'Authorization': self.secretToken
            }
        )
        f = urllib.request.urlopen(req)
        response = f.read()
        jsonO = json.loads(response)
        #print(json.dumps(jsonO, indent=4))
        return jsonO