import urllib
import urllib.parse
import hashlib
import datetime
from random import randint
from Process.TweetPicker import TweetPicker
from Process.PreProcessing import PreProcessing
from Process.SpamFiltering import SpamFiltering
from Classifier.sentimentClassifier import SentimentClassifier


class Main(object):

    def __init__(self, rawKey):
        self.rawKey = rawKey

        if " " not in self.rawKey:
            if not self.rawKey.startswith("#"):
                self.rawKey = "#" + self.rawKey

        self.searchEncoded = urllib.parse.quote(self.rawKey)
        rawId = self.rawKey + "|" + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "|{}".format(randint(0, 100))
        self.runId = hashlib.md5(rawId.encode()).hexdigest()

        self.tweets = []

        self.tweetPicker = TweetPicker()
        self.preProcessing = PreProcessing()
        self.spamFiltering = SpamFiltering()
        self.sentimentClassifier = SentimentClassifier()

    def run(self):

        # Get and Process Tweets
        numberOfTweets = 50
        # TODO -> Uncomment after the spamFix, its working
        self.tweets = self.tweetPicker.getTweets(self.rawKey, numberOfTweets, self.searchEncoded, self.runId)
        """from Process.Tweet import Tweet
        self.tweets = [Tweet("well it's time to pull out the hat and gloves. :wind_face: :person_shrugging: :medium-light_skin_tone: :female_sign:  :sleepy_face: winterishere")]"""

        for tweet in self.tweets:
            self.preProcessing.run(tweet)
            print(tweet.preprocessedTweet)
            self.spamFiltering.run(tweet)

            if not tweet.isSpam:
                #self.sentimentClassifier.run(tweet)
                print("Sentiment: {}".format(tweet.sentiment))
                # TODO -> How we should display this?


Main("WinterIsHere").run()
