from Databases import Database
from Services import SpamSet


def setAsSpam(tweet_id):
    Database.rawTweets.update_item(
        Key={'tweet_id': tweet_id},
        UpdateExpression="set is_spam=:s",
        ExpressionAttributeValues={
            ':s': True
        },
        ReturnValues="UPDATED_NEW"
    )


def run():
    allTweets = Database.getAll(Database.rawTweets)
    spamSet = SpamSet()

    for tweet in allTweets:

        classifyResult = spamSet.classifyTweet(tweet["clear_text"])
        isSpam = thisIsSpam(classifyResult)

        if isSpam:
            setAsSpam(tweet["tweet_id"])


def thisIsSpam(classifyResult):
    print classifyResult
    return False
