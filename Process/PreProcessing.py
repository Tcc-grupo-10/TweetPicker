#from Databases import Database
from Services.TweetCleaner import TweetCleaner
from Services.SpellCheck import SpellCheck


class PreProcessing(object):

    def __init__(self):
        self.tweetCleaner = TweetCleaner()
        self.spellCheck = SpellCheck()

    def run(self, tweet):

        cleanTweet = self.tweetCleaner.processTweet(tweet.rawTweet)
        spellCheck = self.spellCheck.processTweet(cleanTweet)

        tweet.preprocessedTweet = spellCheck
        # TODO -> just insert the clean_tweet field
        # Database.updateItem(tweet, Database.rawTweets)
