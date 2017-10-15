import language_check
import nltk
import string
import re

import enchant
import enchant.checker
from enchant.checker.CmdLineChecker import CmdLineChecker

def spellCheck(tweet):
    tool = language_check.LanguageTool('en-US')
    matches = tool.check(tweet)
    while (len(matches) != 0):
        tweetLog = tweet
        tweet = language_check.correct(tweet, matches)
        matches = tool.check(tweet)
        if tweet == tweetLog:
            break
    return tweet

def untokenize(tokens):
    #text = "".join([" " + i if not i.startswith("'") and i not in string.punctuation else i for i in tokens]).strip()

    text = ' '.join(tokens)
    step1 = text.replace("`` ", '"').replace(" ''", '"').replace('. . .', '...')
    step2 = step1.replace(" ( ", " (").replace(" ) ", ") ")
    step3 = re.sub(r' ([.,:;?!%]+)([ \'"`])', r"\1\2", step2)
    step4 = re.sub(r' ([.,:;?!%]+)$', r"\1", step3)
    step5 = step4.replace(" '", "'").replace(" n't", "n't").replace("can not", "cannot")
    step6 = step5.replace(" ` ", " '")
    text = step6.strip()

    return text

def acronimList():

    return

def acronimCheck():
    tweet = "I'ts gr8 and I've h8g  u... ."
    acronim = 'gr8'
    tokens = nltk.word_tokenize(tweet)
    tokenCounter=-1
    for token in tokens:
        tokenCounter += 1;
        if token == acronim:
            token = 'great'
        tokens[tokenCounter] = token
        print token

    tweet = untokenize(tokens)


    print tweet
    return tweet

acronimCheck()

def grammarCheck(tweet):

    return tweet


def orderCheck(tweet):

    return tweet


def processTweet(tweet):

    tweet = spellCheck(tweet)

    tweet = grammarCheck(tweet)

    tweet = orderCheck(tweet)

    return tweet

