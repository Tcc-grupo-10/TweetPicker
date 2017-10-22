import nltk as nltk
from Databases import Database
from Services import SpamTools


class CreateSpamSet(object):

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

        f = open('../Etc/trainingTest.csv', 'w')
        for a in training_set:
            # print(str(a))
            # print(str(a).encode('utf-8'))
            # wr.writerow([account_id, objective])
            f.write(str(a))
            f.write("\n")

