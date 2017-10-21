import csv
import nltk as nltk
from Services import SpamTools

csvData = []
i = 0

testData = []

with open('../Etc/test2.csv', 'rb') as f:
    reader = csv.DictReader(f)

    for row in reader:
        tweet_id = row["tweet_id"].strip()
        clear_text = row["clear_text"].strip()

        spam = False
        irrelevante = False

        # print "c: {} - s: {} | i: {}".format(clear_text, spam, irrelevante)
        csvData.append((clear_text, spam, irrelevante))


geten = csvData[:20]

for obj in geten:

    if i % 3 == 0:
        spam = "spamA"
    elif i % 3 == 1:
        spam = "spamB"
    else:
        spam = "batata"

    i = i + 1

    testData.append({"clear_text": obj[0], "is_spam": spam})


print testData


def extractFeatures(tweet):
    tweet_words = set(tweet[0])
    features = {}
    for word in tweet[1]:
        features['contains(%s)' % word] = (word in tweet_words)
    return features


def createSet():
    allTweets = testData
    tweets = []
    featureList = []

    for tweet in allTweets:
        sentiment = tweet['is_spam']
        tweet = tweet['clear_text']
        featureVector = SpamTools.getFeatureVector(tweet)
        featureList.extend(featureVector)
        tweets.append((featureVector, sentiment))

    featureList = list(set(featureList))

    # Extract feature vector for all tweets in one shote
    training_set = nltk.classify.util.apply_features(extractFeatures, tweets)

    # Train the classifier
    train = nltk.NaiveBayesClassifier.train(training_set)

    aaa = train.classify(extractFeatures(SpamTools.getFeatureVector("annister army gameofthronesfinale gameofthrones")))

    print "result: {}".format(aaa)


createSet()