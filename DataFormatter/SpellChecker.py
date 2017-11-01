import http
import json
import os
import urllib


class SpellChecker(object):

    def __init__(self):
        self.azure_key = azure_key = os.environ['azure_key']
        self.host = 'api.cognitive.microsoft.com'
        self.path = '/bing/v7.0/spellcheck'
        self.params = {'mkt': 'en-US', 'mode': 'spell', 'text': ''}

    def spell_check(self, text):
        self.params['text'] = text
        headers = {'Ocp-Apim-Subscription-Key': self.azure_key,
                   'Content-Type': 'application/x-www-form-urlencoded'}
        conn = http.client.HTTPSConnection(self.host)
        params = urllib.parse.urlencode(self.params)
        conn.request("POST", self.path, params, headers)
        response = conn.getresponse()
        suggestions = json.loads(response.read())
        for indexSugg, suggestion in enumerate(suggestions["flaggedTokens"]):
            suggestion["suggestions"][0]["suggestion"]
            if suggestion["token"] in text:
                text = text.replace(suggestion["token"], suggestion["suggestions"][0]["suggestion"])
        return text