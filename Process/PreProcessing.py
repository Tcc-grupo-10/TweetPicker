from Services import TweetCleaner, SpellCheck
from Databases import Database


def run(allTweets):

    for tweet in allTweets:
        cleanTweet = TweetCleaner.processTweet(tweet["text"])
        spellCheck = SpellCheck.processTweet(cleanTweet)

        tweet["clean_text"] = spellCheck
        tweet["raw_tweet"] = False
        tweet["preprocessed_tweet"] = True
        Database.updateItem(tweet, Database.rawTweets)

    return allTweets
