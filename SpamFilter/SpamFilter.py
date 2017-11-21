import ast

import numpy as np
from scipy.sparse import csr_matrix
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.svm import LinearSVC


class SpamFilter(object):

    def __init__(self):
        self.featureVector = []
        self.train_set = []
        self.isSpamList = []
        self.stopwords = []
        self.count_vect = CountVectorizer()
        self.tfidf_transformer = TfidfTransformer()

        self.relearn()

    def predict_svm(self, X_new_tfidf):
        clf = LinearSVC().fit(self.train_set, self.isSpamList)
        predicted = clf.predict(X_new_tfidf)

        return predicted

    def getTweetFeatureVector(self, tweet, feature_list):
        features = []
        tweet = self.remove_stopwords(tweet)
        for feature in feature_list:
            if feature in tweet:
                features.append(feature)
        return " ".join(features)

    def predict_items(self, tweets):

        docs_processed = []
        for nd in tweets:
            docs_processed.append(self.getTweetFeatureVector(nd, self.featureVector))

        X_new_counts = self.count_vect.transform(docs_processed)
        X_new_tfidf = self.tfidf_transformer.transform(X_new_counts)

        svm = self.predict_svm(X_new_tfidf)
        return svm

    def remove_stopwords(self, tweet):
        tweetWords = tweet.split(" ")
        notStopwords = list(filter(lambda x: x not in self.stopwords, tweetWords))
        return " ".join(notStopwords)

    def relearn(self):

        loader = np.load('SpamFilter/binaries/train_set.npz')
        self.train_set = csr_matrix((loader['data'], loader['indices'], loader['indptr']), shape=loader['shape'])

        file = open('SpamFilter/binaries/isSpamList.txt', 'r')
        self.isSpamList = ast.literal_eval(file.read())

        file = open('SpamFilter/binaries/featureVector.txt', 'r')
        self.featureVector = ast.literal_eval(file.read())

        file = open('SpamFilter/binaries/tweetsTraining.txt', 'r')
        tweets = ast.literal_eval(file.read())
        X_train_counts = self.count_vect.fit_transform(tweets)
        self.tfidf_transformer.fit_transform(X_train_counts)

        file = open('SpamFilter/binaries/stopwords.txt', 'r')
        for line in file:
            self.stopwords.append(line.replace("\n", ""))

