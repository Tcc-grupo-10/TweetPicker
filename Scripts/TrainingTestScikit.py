import csv

from scipy.sparse import csr_matrix
from sklearn.svm import SVC

from Services import SpamTools
import ast
import operator
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB

import numpy as np

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
targ = []
tweets = []
featureVector = {}


def updateVector(features):
    for feature in features:
        try:
            featureVector[feature] = featureVector[feature] + 1
        except:
            featureVector[feature] = 1


def removeFrequencyFromVector(qtd):
    featureVectors = {k: v for k, v in featureVector.items() if v > qtd}
    fileredVector = sorted(featureVectors.items(), key=operator.itemgetter(1))
    return list(map(lambda x: x[0], fileredVector))


def removeFrequencyFromTweets():
    newTweets = []

    for tweet in tweets:
        newTweets.append(" ".join(list(filter(lambda x: x in featureVector, tweet))))
    return newTweets


for obj in geten:

    if i % 2 == 0:
        spam = True
    else:
        spam = False

    i = i + 1

    testData.append({"clear_text": obj[0], "is_spam": spam})
    ww = SpamTools.getFeatureVector(obj[0], 2, [])
    updateVector(ww)
    tweets.append(ww)
    targ.append(spam)

featureVector = removeFrequencyFromVector(0)
tweets = removeFrequencyFromTweets()
print(featureVector)


count_vect = CountVectorizer()
X_train_counts = count_vect.fit_transform(tweets)

tfidf_transformer = TfidfTransformer()
X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)

def save_sparse_csr(array):
    np.savez('../Etc/trainingTest2.npz', data=array.data, indices=array.indices,
             indptr=array.indptr, shape=array.shape)

def load_sparse_csr():
    loader = np.load('../Etc/trainingTest2.npz')
    return csr_matrix((loader['data'], loader['indices'], loader['indptr']), shape=loader['shape'])

save_sparse_csr(X_train_tfidf)
f = open('../Etc/isSpamList.txt', 'w')
f.write(str(targ))

f = open('../Etc/featureVector.txt', 'w')
f.write(str(featureVector))

f = open('../Etc/tweetsTraining.txt', 'w')
f.write(str(tweets))

training_set = load_sparse_csr()

docs_new = ['are we sure this season is', 'never change, bronn', 'remembering the last episode is in 30 minutes', 'hound was looking for a']
docs_processed = []
for nd in docs_new:
    docs_processed.append(SpamTools.getTweetFeatureVectorString(nd, featureVector))

print("docs_processed: {}".format(docs_processed))

# TODO -> Era isso aqui que eu não tinha colocado na poc
"""count_vect = CountVectorizer()
count_vect.fit_transform(tweets)"""

X_new_counts = count_vect.transform(docs_new)
X_new_tfidf = tfidf_transformer.transform(X_new_counts)


clf = MultinomialNB().fit(training_set, targ)
predicted = clf.predict(X_new_tfidf)

print("\n\nNB:\n")
print("pred: {}".format(predicted))

for doc, category in zip(docs_new, predicted):
    print('%r => %s' % (doc, category))

clfS = SVC().fit(training_set, targ)
predictedS = clfS.predict(X_new_tfidf)

print("\n\nSVM:\n")

print("pred: {}".format(predictedS))

for doc, category in zip(docs_new, predictedS):
    print('%r => %s' % (doc, category))