import csv
from Databases import Database

csvData = []


def spamUpdate(tweet_id, spam, irrelevante, training):
    Database.unTweeterizeTable.update_item(
        Key={'tweet_id': tweet_id},
        UpdateExpression="set is_spam=:s, is_irrelevant=:i, is_training:t",
        ExpressionAttributeValues={
            ':s': spam,
            ':i': irrelevante,
            ':t': training
        },
        ReturnValues="UPDATED_NEW"
    )

with open('test.csv', 'rb') as f:
    reader = csv.DictReader(f)
    for row in reader:
        tweet_id = row["tweet_id"].strip()

        spam = False
        irrelevante = False

        if row["SPAM"].strip() == 'x':
            spam = True

        if row["IRRELEVANTE"].strip() == 'x':
            irrelevante = True

        print ("id: {} - s: {} | i: {}".format(tweet_id, spam, irrelevante))
        csvData.append((tweet_id, spam, irrelevante))


allTweets = Database.getAll(Database.unTweeterizeTable)

for tweet in allTweets:

    tweetCsv = filter(lambda x: x[0] == tweet["tweet_id"], csvData)

    if len(tweetCsv) == 1:
        tweet["is_spam"] = tweetCsv[0][1]
        tweet["is_irrelevant"] = tweetCsv[0][2]
        tweet["is_training"] = True

    # spamUpdate(tweet["tweet_id"], tweet["is_spam"], tweet["is_irrelevant"], tweet["is_training"])
