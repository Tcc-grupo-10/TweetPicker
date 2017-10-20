import os
from Databases import Database
from Services import SpellCheck

allTweets = Database.getAll(Database.unTweeterizeTable)

print len(allTweets)

for tweet in allTweets:
    tweet["untweet"] = tweet["clear_text"]
    tweet["clear_text"] = SpellCheck.processTweet(tweet["untweet"])

    print tweet["untweet"]
    print tweet["clear_text"]
    print "\n\n"