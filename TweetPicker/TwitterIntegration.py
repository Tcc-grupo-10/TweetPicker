import base64
import json
import os
import urllib.parse


class TwitterIntegration(object):
    def __init__(self):
        self._consumerKeyTwitter = os.environ['consumer_key_twitter']
        self._consumerSecretTwitter = os.environ['consumer_secret_twitter']
        self._secretToken = self.get_token_userless("Basic {}".format(
            base64.b64encode((self._consumerKeyTwitter + ":" + self._consumerSecretTwitter).encode('utf-8'))).replace(
            "b'", ""))

    def get_token_userless(self, secret):
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

    def getSearch(self, search_key, count=100):
        search_key = urllib.parse.quote(search_key)
        url = 'https://api.twitter.com/1.1/search/tweets.json?q=' + search_key + "&lang=en&count={}".format(count)

        req = urllib.request.Request(
            url,
            data=None,
            headers={
                'Authorization': self._secretToken
            }
        )
        f = urllib.request.urlopen(req)
        response = f.read()
        jsonO = json.loads(response)
        return jsonO

    def getNextSearch(self, nextUrl):
        url = 'https://api.twitter.com/1.1/search/tweets.json' + nextUrl
        req = urllib.request.Request(
            url,
            data=None,
            headers={
                'Authorization': self._secretToken
            }
        )
        f = urllib.request.urlopen(req)
        response = f.read()
        jsonO = json.loads(response)
        return jsonO
