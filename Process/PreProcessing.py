import Databases.Database
import Services.TweetCleaner
import Services.SpellCheck


def spellCheck(tweet):
    return tweet


def run():

    allTweets = Databases.Database.getAll(Databases.Database.rawTweets)

    for tweet in allTweets:
        cleanTweet = Services.TweetCleaner.processTweet(tweet["text"])
        spellCheck = Services.SpellCheck.processTweet(cleanTweet)

        tweet["clean_text"] = spellCheck
        tweet["raw_tweet"] = False
        tweet["preprocessed_tweet"] = True
        Databases.Database.updateItem(tweet, Databases.Database.rawTweets)
