import csv
from Services import SpamTools
import ast

from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB

import numpy as np
import pandas as pd

"""df = pd.read_csv("../Etc/test2.csv", header = 0)

# put the original column names in a python list
original_headers = list(df.columns.values)

print("original_headers: {}".format(original_headers))

# put the numeric column names in a python list
numeric_headers = list(df.columns.values)

print("numeric_headers: {}".format(numeric_headers))

# create a numpy array with the numeric values for input into scikit-learn
numpy_array = df.as_matrix()

print("numpy_array: {}".format(numpy_array))
"""

csvData = []
i = 0
testData = []

with open('../Etc/test2.csv', 'rt', encoding="utf8") as f:
    reader = csv.DictReader(f)

    for row in reader:
        tweet_id = row["tweet_id"].strip()
        clear_text = row["clear_text"].strip()

        spam = False
        irrelevante = False

        # print "c: {} - s: {} | i: {}".format(clear_text, spam, irrelevante)
        csvData.append((clear_text, spam))

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

numpy_array = np.asarray(testData)

targ = []
tweets = []
for t in numpy_array:
    tweets.append(t["clear_text"])
    targ.append(t["is_spam"])

print("targ: {}".format(targ))


"""

categories = ['comp.graphics', 'sci.med']
twenty_train = fetch_20newsgroups(subset='train', categories=categories, shuffle=True, random_state=42)

aa = twenty_train.target

print(aa)

"""

count_vect = CountVectorizer()
X_train_counts = count_vect.fit_transform(tweets)
print("X_train_counts: {}".format(X_train_counts))

tf_transformer = TfidfTransformer(use_idf=False).fit(X_train_counts)
X_train_tf = tf_transformer.transform(X_train_counts)
X_train_tf.shape


tfidf_transformer = TfidfTransformer()
X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)
X_train_tfidf.shape



docs_new = ['are we sure this season is', 'never change, bronn', 'remembering the last episode is in 30 minutes']
X_new_counts = count_vect.transform(docs_new)
X_new_tfidf = tfidf_transformer.transform(X_new_counts)


clf = MultinomialNB().fit(X_train_tfidf, targ)
predicted = clf.predict(X_new_tfidf)

for doc, category in zip(docs_new, predicted):
    print('%r => %s' % (doc, category))

"""
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


def extractFeatureList(text, n_gram, stop_words ):
    text :

def processFeatureList(featureList, n_gram = 1, stop_words = True, frequency = 1  ):
"""
