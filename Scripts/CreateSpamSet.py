from Databases import Database
from Services import SpamTools
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer


class CreateSpamSet(object):

    def __init__(self, useStopwords = False, nGram = 1, frequencyMin = 1):

        self.featureVector = []
        self.tweets = []
        self.isSpamList = []
        self.frequencyMin = frequencyMin
        self.nGram = nGram
        self.stopwords = SpamTools.getStopwords(useStopwords)
        self.createSet()

        self.testData = []

    def createSet(self):
        allTweets = Database.getAll(Database.unTweeterizeTable)
        # TODO -> Check this filter
        allTweets = list(filter(lambda x: x.get("is_training", False), allTweets))

        for tweet in allTweets:
            self.testData.append({"clear_text": tweet["clear_text"], "is_spam": tweet["is_spam"]})
            tweetFV = SpamTools.getFeatureVector(tweet["clear_text"], self.nGram, self.stopwords)
            self.featureVector = SpamTools.updateVector(tweetFV, self.featureVector)
            self.tweets.append(tweetFV)
            self.isSpamList.append(tweet["is_spam"])

        self.featureVector = SpamTools.removeFrequencyFromVector(self.frequencyMin, self.featureVector)
        self.tweets = SpamTools.removeFrequencyFromTweets(self.featureVector, self.tweets)

        count_vect = CountVectorizer()
        X_train_counts = count_vect.fit_transform(self.tweets)

        tfidf_transformer = TfidfTransformer()
        X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)

        SpamTools.save_sparse_csr(X_train_tfidf)
        f = open('../Etc/isSpamList.txt', 'w')
        f.write(str(self.isSpamList))

        f = open('../Etc/featureVector.txt', 'w')
        f.write(str(self.featureVector))


CreateSpamSet()
