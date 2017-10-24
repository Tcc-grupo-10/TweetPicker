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
        self.training_set = []
        self.isSpamList = []
        self.createSet()

    def createSet(self):
        self.training_set = SpamTools.load_sparse_csr()

        o = open('../Etc/isSpamList.txt', 'r')
        self.isSpamList = ast.literal_eval(o.read())

    def classifyTweet(self, tweet):
        docs_processed = []
        docs_processed.append(" ".join(SpamTools.getFeatureVector(tweet, 2, [])))

        count_vect = CountVectorizer()
        tfidf_transformer = TfidfTransformer()

        X_new_counts = count_vect.transform(docs_processed)
        X_new_tfidf = tfidf_transformer.transform(X_new_counts)

        clf = MultinomialNB().fit(self.training_set, self.isSpamList)
        predicted = clf.predict(X_new_tfidf)

        # TODO -> how to return that?
        for doc, category in zip(docs_processed, predicted):
            print('%r => %s' % (doc, category))



