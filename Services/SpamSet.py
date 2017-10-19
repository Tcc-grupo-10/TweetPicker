import nltk as nltk
from Databases import Database
from Services import SpamTools


class SpamSet(object):

    def __init__(self):
        self.featureList = []
        self.nbClassifier = self.createSet()

    def extractFeatures(self, tweet):
        tweet_words = set(tweet)
        features = {}
        for word in self.featureList:
            features['contains(%s)' % word] = (word in tweet_words)
        return features

    def createSet(self):

        allTweets = Database.getAll(Database.unTweeterizeTable)
        tweets = []

        for tweet in allTweets:

            sentiment = tweet['is_spam']
            tweet = tweet['clear_text']
            featureVector = SpamTools.getFeatureVector(tweet)
            self.featureList.extend(featureVector)
            tweets.append((featureVector, sentiment))

        self.featureList = list(set(self.featureList))

        # Extract feature vector for all tweets in one shote
        training_set = nltk.classify.util.apply_features(self.extractFeatures, tweets)

        # Train the classifier
        return nltk.NaiveBayesClassifier.train(training_set)

    def classifyTweet(self, tweet):
        return self.nbClassifier.classify(self.extractFeatures(SpamTools.getFeatureVector(tweet)))
