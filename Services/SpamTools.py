import re
import operator
import operator
import numpy as np
from scipy.sparse import csr_matrix

def replaceTwoOrMore(s):
    # look for 2 or more repetitions of character and replace with the character itself
    #pattern = re.compile(r"(.)\1{1,}", re.DOTALL)

    arr = " ".join(s)
    return arr

    # TODO -> check this
    # return pattern.sub(r"\1\1", arr)


def ngrams(input, n, stopwords):
    output = []
    input = list(filter(lambda x: x not in stopwords, input))
    for i in range(len(input)-n+1):
        output.append(input[i:i+n])

    return output


def getFeatureVector(tweet, nGram, stopwords=[]):
    featureVector = []

    pattern = r"[{}]".format("!#$%&\()*+,-./;<=>?@[\\]^`{|}~")
    tweet = re.sub(pattern, "", tweet)

    words = ngrams(tweet.split(), nGram, stopwords)
    for w in words:
        w = replaceTwoOrMore(w)
        # trim
        w = w.strip()
        # check if the word stats with an alphabet
        # val = re.search(r"^[a-zA-Z][a-zA-Z0-9]*$", w)

        if w not in stopwords:
            featureVector.append(w.lower())

    return featureVector


def getStopwords(swActive):
    if swActive:
        arr = []
        file = open('../Etc/stopwords.txt', 'r')
        for line in file:
            line = line.strip("\n")
            arr.append(line)
        return arr
    else:
        return []

def getFeatureList():
    file = open('Etc/featureVector.txt', 'r')
    line = eval(file.readline())
    return line


def updateVector(features, featureVector):
    for feature in features:
        try:
            featureVector[feature] = featureVector[feature] + 1
        except:
            featureVector[feature] = 1
    return features


def removeFrequencyFromVector(qtd, featureVector):
    featureVectors = {k: v for k, v in featureVector.items() if v > qtd}
    fileredVector = sorted(featureVectors.items(), key=operator.itemgetter(1))
    return fileredVector


def removeFrequencyFromTweets(featureVector, tweets):
    newTweets = []
    justWords = list(map(lambda x: x[0], featureVector))

    for tweet in tweets:
        newTweets.append(" ".join(list(filter(lambda x: x in justWords, tweet))))
    return newTweets


def getTweetFeatureVector(tweet, feature_list):
    features = []
    for feature in feature_list:
        if feature in tweet:
            features.append(feature)

    print("features: {}".format(features))
    return features


def getTweetFeatureVectorString(tweet, feature_list):
    return " ".join(getTweetFeatureVector(tweet, feature_list))


def save_sparse_csr(array):
    np.savez('Etc/trainingTest2.npz', data=array.data, indices=array.indices,
             indptr=array.indptr, shape=array.shape)


def load_sparse_csr():
    loader = np.load('Etc/trainingTest2.npz')
    return csr_matrix((loader['data'], loader['indices'], loader['indptr']), shape=loader['shape'])