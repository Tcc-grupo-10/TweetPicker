import language_check
import nltk
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

def acronimCheck():
    tweet = "teste"
    enchant.add(tweet)

    return tweet

def tokenizer():
    tweet = ''
    tokens = nltk.word_tokenize(tweet)
    return tokens

def grammarCheck(tweet):

    return tweet


def orderCheck(tweet):

    return tweet


def processTweet(tweet):

    tweet = spellCheck(tweet)

    tweet = grammarCheck(tweet)

    tweet = orderCheck(tweet)

    return tweet

