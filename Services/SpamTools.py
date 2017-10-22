import re


def replaceTwoOrMore(s):
    # look for 2 or more repetitions of character and replace with the character itself
    pattern = re.compile(r"(.)\1{1,}", re.DOTALL)
    return pattern.sub(r"\1\1", s)


def getFeatureVector(tweet, nGram, stopwords = []):
    featureVector = []
    words = tweet.split()
    for w in words:
        w = replaceTwoOrMore(w)
        # strip punctuation
        w = w.strip('\'"?,.')
        # check if the word stats with an alphabet
        val = re.search(r"^[a-zA-Z][a-zA-Z0-9]*$", w)

        if w not in stopwords and val is not None:
            featureVector.append(w.lower())

    return featureVector


def getStopwords(swActive):
    if swActive:
        arr = []
        file = open('../Etc/stopwords.txt', 'r')
        for line in file:
            arr.append(line)
        return arr
    else:
        return []
