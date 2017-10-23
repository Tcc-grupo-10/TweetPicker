import csv
from Services import SpamTools
import ast

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

for obj in geten:

    if i % 3 == 0:
        spam = "spamA"
    elif i % 3 == 1:
        spam = "spamB"
    else:
        spam = "batata"

    i = i + 1

    testData.append({"clear_text": obj[0], "is_spam": spam})
    ww = SpamTools.getFeatureVector(obj[0], 2, [])
    tweets.append(" ".join(ww))
    targ.append(spam)


count_vect = CountVectorizer()
X_train_counts = count_vect.fit_transform(tweets)

tf_transformer = TfidfTransformer(use_idf=False).fit(X_train_counts)
X_train_tf = tf_transformer.transform(X_train_counts)

tfidf_transformer = TfidfTransformer()
X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)

docs_new = ['are we sure this season is', 'never change, bronn', 'remembering the last episode is in 30 minutes', 'hound was looking for a']
docs_processed = []
for nd in docs_new:
    docs_processed.append(" ".join(SpamTools.getFeatureVector(nd, 2, [])))

X_new_counts = count_vect.transform(docs_processed)
X_new_tfidf = tfidf_transformer.transform(X_new_counts)


clf = MultinomialNB().fit(X_train_tfidf, targ)
predicted = clf.predict(X_new_tfidf)

for doc, category in zip(docs_new, predicted):
    print('%r => %s' % (doc, category))

