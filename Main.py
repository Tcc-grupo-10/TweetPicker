import hashlib
import datetime
from tkinter import ACTIVE

from Classifier.sentimentClassifier import SentimentClassifier
from DataFormatter.DataFormatter import DataFormatter
from Database.DatabaseConnector import DatabaseConnector
from PreProcessor.PreProcessor import PreProcessor
from SpamFilter.SpamFilter import SpamFilter
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
        self.preProcessing = PreProcessor()
        self.dataFormatter = DataFormatter()

        self.spamFilter = SpamFilter()
        self.sentimentClassifier = SentimentClassifier()

    def run(self):
        numberOfTweets = 10
        self.interface.log("Pegando {} Tweets sobre \"{}\"".format(numberOfTweets, self.search_key))

        self.tweets = self.tweetPicker.search_tweets(self.search_key, numberOfTweets)

        self.interface.log("Processando Tweets:\n")
        for tweet in self.tweets:
            print("original: " + tweet.original_tweet)

            # PreProcessing
            (pre_processed_text, emoji_list) = self.preProcessing.pre_process_tweet(tweet.original_tweet)
            tweet.emojis = emoji_list
            tweet.preprocessed_tweet = self.dataFormatter.format_data(pre_processed_text)

            self.db.save_preprocessed_tweet(tweet)
            print("preprocessed: " + tweet.preprocessed_tweet)
            print("emojis: " + str(tweet.emojis))

            # Formatting
            tweet.formatted_tweet = self.dataFormatter.format_data(tweet.preprocessed_tweet)
            self.db.save_formatted_tweet(tweet)

            print("formatted: " + str(tweet.formatted_tweet))
            print("\n")

        texts = list(map(lambda x: x.formatted_tweet, self.tweets))
        spam_list = self.spamFilter.predict_items(texts)

        for (index, tw), spam in zip(enumerate(self.tweets), spam_list):
            tw.is_spam = spam

            if tw.is_spam == "0":
                tw.sentiment = self.sentimentClassifier.run(tw.formatted_tweet, tw.emojis)

            self.interface.log("Tweet: {}\nText: {}\nSentiment: {}\n".format(index + 1, tw.formatted_tweet, tw.sentiment))

        self.interface.startButton.configure(state=ACTIVE)
