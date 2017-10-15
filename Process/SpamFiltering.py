from Databases import Database


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

    for tweet in allTweets:

        # TODO -> How we are going to do that?
        isSpam = False

        if isSpam:
            setAsSpam(tweet["tweet_id"])
