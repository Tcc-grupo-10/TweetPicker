import re
import string


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
            arr.append(line)
        return arr
    else:
        return []
