import nltk as nltk
from Services import SpamTools
import ast


class SpamSet(object):

    def __init__(self, useStopwords = False, nGram = 1):
        self.featureList = []
        self.nGram = nGram
        self.stopwords = SpamTools.getStopwords(useStopwords)
        self.nbClassifier = self.createSet()

    def extractFeatures(self, tweet):
        tweet_words = set(tweet)
        features = {}
        # TODO -> Check this featureList.. I think that this is empty
        for word in self.featureList:
            features['contains(%s)' % word] = (word in tweet_words)
        return features

    def createSet(self):

        training_set = []
        file = open('../Etc/trainingTest.csv', 'r')
        for line in file:
            training_set.append(ast.literal_eval(line))

        # Train the classifier
        return nltk.NaiveBayesClassifier.train(training_set)

    def classifyTweet(self, tweet):
        return self.nbClassifier.classify(self.extractFeatures(SpamTools.getFeatureVector(tweet, self.nGram)))
