from Databases import Database
from Services import SpellCheck


def spellUpdate(tweet_id, clear_text, untweet_text):
    Database.unTweeterizeTable.update_item(
        Key={'tweet_id': tweet_id},
        UpdateExpression="set clear_text=:c, untweet_text=:u",
        ExpressionAttributeValues={
            ':c': clear_text,
            ':u': untweet_text
        },
        ReturnValues="UPDATED_NEW"
    )

allTweets = Database.getAll(Database.unTweeterizeTable)

print("\n\nallTweets b4: {}".format(len(allTweets)))

allTweets = list(filter(lambda x: x.get("untweet_text", "_NULL_") == "_NULL_", allTweets))

tot = len(allTweets)

print("allTweets af: {}".format(tot))

for tweet in allTweets:
    tot -= 1
    tweet["untweet_text"] = tweet["clear_text"]
    tweet["clear_text"] = SpellCheck.processTweet(tweet["untweet_text"])

    print(tweet["untweet_text"])
    print(tweet["clear_text"])
    print("{}\n\n".format(tot))

    spellUpdate(tweet["tweet_id"], tweet["clear_text"], tweet["untweet_text"])

print("\n\nACABOOOOU\n\n")