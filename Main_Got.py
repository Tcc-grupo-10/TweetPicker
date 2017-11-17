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
        self.sentimentClassifier = SentimentClassifier()

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

        file_writer = csv.writer(open("GOT_RUN.csv", 'w', newline=''))
        file_writer.writerow(['tweet_id', 'formatted_tweet', 'spam_label', '|', 'pleasantness', 'attention',
                              'sensitivity', 'aptitude', 'polarity_intense', 'emojis'])

        for tw, spam in zip(self.tweets, spam_list):
            tw["is_spam"] = spam

            if tw["is_spam"] == "0":
                tweet["sentiment"] = self.sentimentClassifier.run(tweet["formatted_tweet"], tweet["emojis"])

            file_writer.writerow([tw['tweet_id'],
                                  tw['formatted_tweet'],
                                  tw['is_spam'],
                                  '|',
                                  tw['sentiment'].get('pleasantness', '-'),
                                  tw['sentiment'].get('attention', '-'),
                                  tw['sentiment'].get('sensitivity', '-'),
                                  tw['sentiment'].get('aptitude', '-'),
                                  tw['sentiment'].get('polarity_intense', '-'),
                                  tw['sentiment'].get('emojis', '-')])

    def load_got_tweets(self):
        return DatabaseConnector("UnTweeterize").get_all()

Main_Got().run()
