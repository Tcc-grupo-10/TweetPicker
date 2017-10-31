import nltk as nltk
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import SVC

from Services import SpamTools
import ast

class SpamSet(object):

    def __init__(self, useStopwords = False, nGram = 1):
        self.featureList = []
        self.nGram = nGram
        self.stopwords = SpamTools.getStopwords(useStopwords)
        self.featureList = SpamTools.getFeatureList()
        self.training_set = []
        self.isSpamList = []
        self.tweetsTraining = []
        self.loadSet()

    def loadSet(self):
        self.training_set = SpamTools.load_sparse_csr()

        o = open('Etc/isSpamList.txt', 'r')
        self.isSpamList = ast.literal_eval(o.read())

        o = open('Etc/tweetsTraining.txt', 'r')
        self.tweetsTraining = ast.literal_eval(o.read())

    def classifyTweet(self, tweet):
        docs_processed = SpamTools.getTweetFeatureVector(tweet, self.featureList)

        if len(docs_processed) == 0:
            print("Do not contains features to process.. what do we do?")
            return "Do not contains features to process.. what do we do?"
        else:
            print("features: {}".format(docs_processed))
            count_vect = CountVectorizer()
            X_train_counts = count_vect.fit_transform(self.tweetsTraining)

            tfidf_transformer = TfidfTransformer()
            tfidf_transformer.fit_transform(X_train_counts)

            X_new_counts = count_vect.transform(docs_processed)
            X_new_tfidf = tfidf_transformer.transform(X_new_counts)

            clf = MultinomialNB().fit(self.training_set, self.isSpamList)
            predicted = clf.predict(X_new_tfidf)

            return predicted[0]



