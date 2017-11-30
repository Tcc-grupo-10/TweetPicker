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
        self.search_key = search_key
        self.interface = interface
        self.interface.log("Processo Iniciado")

        rawId = self.search_key + "|" + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.runId = hashlib.md5(rawId.encode()).hexdigest()

        self.tweets = []
        self.db = DatabaseConnector()
        self.tweet_sentiments = []

        self.tweetPicker = TweetSearcher(self.runId, self.db, self.interface)
        self.preProcessing = PreProcessor()
        self.dataFormatter = DataFormatter()

        self.spamFilter = SpamFilter()
        self.sentimentClassifier = SentimentClassifier()

    def run(self):
        numberOfTweets = 15
        self.interface.log("Pegando {} Tweets sobre \"{}\"".format(numberOfTweets, self.search_key))

        self.tweets = self.tweetPicker.search_tweets(self.search_key, numberOfTweets)

        self.interface.log("Processando Tweets:\n")
        for tweet in self.tweets:
            print("original: " + tweet.original_tweet)

            # PreProcessing
            (pre_processed_text, emoji_list) = self.preProcessing.pre_process_tweet(tweet.original_tweet)
            tweet.emojis = emoji_list
            tweet.preprocessed_tweet = pre_processed_text

            # self.db.save_preprocessed_tweet(tweet)
            print("preprocessed: " + tweet.preprocessed_tweet)
            print("emojis: " + str(tweet.emojis))

            # Formatting
            tweet.formatted_tweet = self.dataFormatter.format_data(tweet.preprocessed_tweet)
            # self.db.save_formatted_tweet(tweet)

            print("formatted: " + str(tweet.formatted_tweet))
            print("\n")

        texts = list(map(lambda x: x.formatted_tweet, self.tweets))
        spam_list = self.spamFilter.predict_items(texts)
        spam_amount = len(list(filter(lambda x: x == "1", spam_list)))

        self.interface.log("Total tweets: {}\nTotal spam: {}\nTotal normal: {}\n".
                           format(len(spam_list), spam_amount, len(spam_list) - spam_amount))

        for (index, tw), spam in zip(enumerate(self.tweets), spam_list):
            tw.is_spam = spam
            # self.db.save_is_spam(tw)
            if tw.is_spam == "0":
                tw.sentiment = self.sentimentClassifier.run(tw.formatted_tweet, tw.emojis)
                # self.db.save_sentiment(tw)
                self.tweet_sentiments.append(tw.sentiment)

            self.interface.log("Tweet: {}\nSpam: {}\nText: {}\nSentiment: {}\n".format(index + 1, tw.is_spam, tw.formatted_tweet, tw.sentiment))

        self.interface.startButton.configure(state=ACTIVE)

        self.avg_sentiment()

        self.interface.log("\nProcesso Finalizado")

    def avg_sentiment(self):

        sentiment_avg = {'pleasantness': 0.0, 'attention': 0.0, 'sensitivity': 0.0,
                         'aptitude': 0.0, 'polarity_intense': 0.0, "emoji": 0.0}

        sentic_filtered = list(filter(lambda x: x is not None, self.tweet_sentiments))

        emojis_uses = 0
        sentic_uses = 0

        for sentic in sentic_filtered:
            if sentic['pleasantness'] != '' and sentiment_avg['pleasantness'] != '':
                sentic_uses += 1
                sentiment_avg['pleasantness'] += float(sentic['pleasantness'])
                sentiment_avg['attention'] += float(sentic['attention'])
                sentiment_avg['sensitivity'] += float(sentic['sensitivity'])
                sentiment_avg['aptitude'] += float(sentic['aptitude'])
                sentiment_avg['polarity_intense'] += float(sentic['polarity_intense'])

            if sentic['emoji'] is not None:
                emojis_uses += 1
                sentiment_avg['emoji'] += float(sentic['emoji'])

        if sentic_uses > 0:
            sentiment_avg['pleasantness'] /= float(len(sentic_filtered))
            sentiment_avg['attention'] /= float(len(sentic_filtered))
            sentiment_avg['sensitivity'] /= float(len(sentic_filtered))
            sentiment_avg['aptitude'] /= float(len(sentic_filtered))
            sentiment_avg['polarity_intense'] /= float(len(sentic_filtered))

        if emojis_uses > 0:
            sentiment_avg['emoji'] /= float(len(sentic_filtered))

        elif emojis_uses == 0 and sentic_uses == 0:
            sentiment_avg = None

        self.interface.log("Média dos Sentimentos:\n{}".format(sentiment_avg))
