import ast

import numpy as np
from scipy.sparse import csr_matrix
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import SVC


class SpamFilter(object):

    def __init__(self):
        self.featureVector = []
        self.train_set = []
        self.isSpamList = []
        self.count_vect = CountVectorizer()
        self.tfidf_transformer = TfidfTransformer()

        self.relearn()

    def predict_nb(self, X_new_tfidf):
        clf = MultinomialNB().fit(self.train_set, self.isSpamList)
        predicted = clf.predict(X_new_tfidf)

        return predicted

    def predict_svm(self, X_new_tfidf):
        clf = SVC().fit(self.train_set, self.isSpamList)
        predicted = clf.predict(X_new_tfidf)

        return predicted

    def getTweetFeatureVector(self, tweet, feature_list):
        features = []
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

        nb = self.predict_nb(X_new_tfidf)
        # svm = self.predict_svm(X_new_tfidf)

        print("nb_: {}".format(nb))
        # print("svm: {}".format(svm))

        return nb

    def relearn(self):

        loader = np.load('SpamFilter/binaries/train_set.npz')
        self.train_set = csr_matrix((loader['data'], loader['indices'], loader['indptr']), shape=loader['shape'])

        o = open('SpamFilter/binaries/isSpamList.txt', 'r')
        self.isSpamList = ast.literal_eval(o.read())

        file = open('SpamFilter/binaries/featureVector.txt', 'r')
        self.featureVector = ast.literal_eval(file.read())

        file = open('SpamFilter/binaries/tweetsTraining.txt', 'r')
        tweets = ast.literal_eval(file.read())
        X_train_counts = self.count_vect.fit_transform(tweets)
        self.tfidf_transformer.fit_transform(X_train_counts)

