import csv
import hashlib
import datetime

from Classifier.sentimentClassifier import SentimentClassifier
from DataFormatter.DataFormatter import DataFormatter
from Database.DatabaseConnector import DatabaseConnector
from PreProcessor.PreProcessor import PreProcessor
from SpamFilter.SpamFilter import SpamFilter
from TweetPicker.TweetSearcher import TweetSearcher


class Main_Got(object):
    def __init__(self):
        print("Initializing Process...")

        rawId = "got|" + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.runId = hashlib.md5(rawId.encode()).hexdigest()

        self.tweets = self.load_got_tweets()
        self.db = DatabaseConnector()

        self.preProcessing = PreProcessor()
        self.dataFormatter = DataFormatter()

        self.spamFilter = SpamFilter()
        # self.sentimentClassifier = SentimentClassifier(self.runId, self.db)

    def run(self):

        for tweet in self.tweets:
            print("original: " + tweet["raw_text"])

            # PreProcessing
            (pre_processed_text, emoji_list) = self.preProcessing.pre_process_tweet(tweet["raw_text"])
            tweet["emojis"] = emoji_list
            tweet["preprocessed_tweet"] = self.dataFormatter.format_data(pre_processed_text)

            # self.db.save_preprocessed_tweet(tweet)
            print("preprocessed: " + tweet["preprocessed_tweet"])
            print("emojis: " + str(tweet["emojis"]))

            # Formatting
            tweet["formatted_tweet"] = self.dataFormatter.format_data(tweet["preprocessed_tweet"])
            # self.db.save_formatted_tweet(tweet)

            print("formatted: " + str(tweet["formatted_tweet"]))
            print("\n")

        texts = list(map(lambda x: x["formatted_tweet"], self.tweets))
        spam_list = self.spamFilter.predict_items(texts)

        for tw, spam in zip(self.tweets, spam_list):
            tw["is_spam"] = spam

        print(self.tweets)

    def load_got_tweets(self):
        return DatabaseConnector("UnTweeterize").get_all()

Main_Got().run()