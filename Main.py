import hashlib
import datetime

from Classifier.sentimentClassifier import SentimentClassifier
from DataFormatter.DataFormatter import DataFormatter
from Database.DatabaseConnector import DatabaseConnector
from PreProcessor.PreProcessor import PreProcessor
from TweetPicker.TweetSearcher import TweetSearcher


class Main(object):
    def __init__(self, search_key, interface):
        print("Initializing Process...")
        self.search_key = search_key
        self.interface = interface

        rawId = self.search_key + "|" + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.runId = hashlib.md5(rawId.encode()).hexdigest()

        self.tweets = []
        self.db = DatabaseConnector()
        self.tweetPicker = TweetSearcher(self.runId, self.db, self.interface)
        self.preProcessing = PreProcessor(self.runId, self.db)
        self.dataFormatter = DataFormatter(self.runId, self.db)
        # self.spamFiltering = SpamFiltering(self.runId, self.db)
        # self.sentimentClassifier = SentimentClassifier(self.runId, self.db)

    def run(self):
        # Get and Process Tweets
        numberOfTweets = 10
        self.interface.log("Pegando {} Tweets sobre \"{}\"".format(numberOfTweets, self.search_key))
        # TODO -> Uncomment after the spamFix, its working

        self.tweets = self.tweetPicker.search_tweets(self.search_key, numberOfTweets)

        for tweet in self.tweets:
            print("original: " + tweet.original_tweet)
            self.preProcessing.pre_process_tweet(tweet)
            print("preprocessed: " + tweet.preprocessed_tweet)
            print("emojis :" + str(tweet.emojis))

            self.dataFormatter.format_data(tweet)
            print("formatted :" + str(tweet.formatted_tweet))
            print("\n")
