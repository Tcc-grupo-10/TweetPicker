import concurrent.futures
import csv
import datetime
import multiprocessing

import _thread

import numpy as np
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import SVC

from DataFormatter.DataFormatter import DataFormatter
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer

from PreProcessor.PreProcessor import PreProcessor
from SpamFilter import Tools


class SpamSet(object):
    def __init__(self, useStopwords=True, nGram=2, frequencyMin=1):

        print("Inicio: {}".format(datetime.datetime.now()))

        self.featureVector = []
        self.tweets = []
        self.frequencyMin = frequencyMin
        self.nGram = nGram
        self.useStopwords = useStopwords
        self.stopwords = Tools.getStopwords(useStopwords)

        self.preProcessing = PreProcessor()
        self.dataFormatter = DataFormatter()

        self.trainData = []
        self.testData = []

        self.load_test_csv()
        self.load_train_csv()

        # predict vars
        self.train_set = []
        self.isSpamList = []
        self.X_train_counts = None
        self.count_vect = CountVectorizer()
        self.tfidf_transformer = TfidfTransformer()

        self.learn()

    def learn(self):

        print("Aprendendo: {}".format(datetime.datetime.now()))

        featureVectorCount = {}
        for (text, label) in self.trainData:
            tweetFV = Tools.getFeatureVector(text, self.nGram, self.stopwords)
            self.featureVector = Tools.updateVector(tweetFV, featureVectorCount)
            self.tweets.append(tweetFV)
            self.isSpamList.append(label)
        print("featureVectorCount: {}".format(datetime.datetime.now()))

        featureVectorCount = Tools.removeFrequencyFromVector(self.frequencyMin, featureVectorCount)
        print("Feature Vector Count: {}".format(datetime.datetime.now()))

        self.featureVector = Tools.getVectorWithoutCount(featureVectorCount)
        self.tweets = Tools.removeFrequencyFromTweets(self.featureVector, self.tweets)
        print("Removing Frequency From Tweets: {}".format(datetime.datetime.now()))

        self.X_train_counts = self.count_vect.fit_transform(self.tweets)
        self.train_set = self.tfidf_transformer.fit_transform(self.X_train_counts)

        print("Aprendeu: {}".format(datetime.datetime.now()))

    def predict_nb(self, X_new_tfidf):
        clf = MultinomialNB().fit(self.train_set, self.isSpamList)
        predicted = clf.predict(X_new_tfidf)

        return predicted

    def predict_svm(self, X_new_tfidf):
        clf = SVC().fit(self.train_set, self.isSpamList)
        predicted = clf.predict(X_new_tfidf)

        return predicted

    def predict_all(self):
        self.predict_item(self.testData)

    def predict_item(self, tweets):

        file_name = '../Etc/sw_{}_ng_{}_fr_{}.csv'.format(self.useStopwords, self.nGram, self.frequencyMin)
        file_writer = csv.writer(open(file_name, 'w', newline=''))
        file_writer.writerow(["tweet_id", "tweet", "original", "NB", "SVM"])

        docs_processed = []
        for nd in tweets:
            without_topwords = self.remove_stopwords(nd[0])
            docs_processed.append(Tools.getTweetFeatureVector(without_topwords, self.featureVector))
        print("docs_processed end: {}".format(datetime.datetime.now()))

        X_new_counts = self.count_vect.transform(docs_processed)
        X_new_tfidf = self.tfidf_transformer.transform(X_new_counts)
        print("transforms: {}".format(datetime.datetime.now()))

        nb = self.predict_nb(X_new_tfidf)
        svm = self.predict_svm(X_new_tfidf)

        print("Saving Dataset: {}".format(datetime.datetime.now()))
        self.save_dataset()


        print("nb_: {}".format(nb))
        print("svm: {}".format(svm))

        for tweet, n, s in zip(tweets, nb, svm):
            print("original: {}| nb: {}| svm: {}".format(tweet[1], n, s))
            file_writer.writerow([tweet[2],
                                  tweet[0],
                                  tweet[1],
                                  n,
                                  s])

    def save_in_csv(self, tweet_results, file_writer):
        file_writer.writerow([tweet_results[0][2],
                              tweet_results[0][0],
                              tweet_results[0][1],
                              tweet_results[1],
                              tweet_results[2]])

    def save_dataset(self):
        np.savez('../SpamFilter/binaries/train_set.npz', data=self.train_set.data, indices=self.train_set.indices,
                 indptr=self.train_set.indptr, shape=self.train_set.shape)

        f = open('../SpamFilter/binaries/isSpamList.txt', 'w')
        f.write(str(self.isSpamList))

        f = open('../SpamFilter/binaries/featureVector.txt', 'w')
        f.write(str(self.featureVector))

        f = open('../SpamFilter/binaries/tweetsTraining.txt', 'w')
        f.write(str(self.tweets))

    def remove_stopwords(self, tweet):
        tweetWords = tweet.split(" ")
        notStopwords = list(filter(lambda x: x not in self.stopwords, tweetWords))
        return " ".join(notStopwords)

    def load_test_csv(self):
        with open('../Etc/teste.csv', 'rt', encoding="utf8") as f:
            reader = csv.DictReader(f)

            for row in reader:
                id = row["tweet_id"].strip()
                text = row["text"].strip()
                label = row["label"].strip()

                (text, emojis) = self.preProcessing.pre_process_tweet(text)
                text = self.dataFormatter.format_data(text)

                self.testData.append((text, label, id))

    def load_train_csv(self):
        with open('../Etc/treino.csv', 'rt', encoding="utf8") as f:
            reader = csv.DictReader(f)

            for row in reader:
                text = row["text"].strip()
                label = row["label"].strip()

                (text, emojis) = self.preProcessing.pre_process_tweet(text)
                text = self.dataFormatter.format_data(text)

                self.trainData.append((text, label))


ss1 = SpamSet(useStopwords=True, nGram=1, frequencyMin=1)
ss1.predict_all()

ss2 = SpamSet(useStopwords=False, nGram=1, frequencyMin=1)
ss2.predict_all()

ss3 = SpamSet(useStopwords=True, nGram=2, frequencyMin=1)
ss3.predict_all()

ss4 = SpamSet(useStopwords=False, nGram=2, frequencyMin=1)
ss4.predict_all()

print("Fim: {}".format(datetime.datetime.now()))
