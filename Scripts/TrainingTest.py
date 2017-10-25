import csv
import nltk as nltk
from Services import SpamTools
import ast

csvData = []
i = 0

testData = []

with open('../Etc/test2.csv', 'rt', encoding="utf8") as f:
    reader = csv.DictReader(f)
    # csv.reader

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


print(testData)



def createSet():
    allTweets = testData
    tweets = []
    featureList = []


    def extractFeatures(tweet):
        tweet_words = set(tweet)
        features = {}
        for word in featureList:
            features['contains(%s)' % word] = (word in tweet_words)
        return features


    for tweet in allTweets:
        sentiment = tweet['is_spam']
        tweet = tweet['clear_text']
        featureVector = SpamTools.getFeatureVector(tweet, 3, [])
        featureList.extend(featureVector)
        tweets.append((featureVector, sentiment))

    featureList = list(set(featureList))

    # Extract feature vector for all tweets in one shote
    training_set = nltk.classify.util.apply_features(extractFeatures, tweets)

    f = open('../Etc/trainingTest.csv', 'w')
    for a in training_set:
        f.write(str(a))
        f.write("\n")

    qwe = []

    o = open('../Etc/trainingTest.csv', 'r')
    for line in o:
        qwe.append(ast.literal_eval(line))
        print(line)



    # Train the classifier

    # print(qwe)
    train = nltk.NaiveBayesClassifier.train(qwe)

    aaa = train.classify(extractFeatures(SpamTools.getFeatureVector("legit twitter and instagram", 3)))

    print("\n\nresult: {}\n\n".format(aaa))


createSet()


"""def extractFeatureList(text, n_gram, stop_words ):
    text :

def processFeatureList(featureList, n_gram = 1, stop_words = True, frequency = 1  ):"""
