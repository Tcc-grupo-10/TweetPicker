import csv
from Databases import Database
import re

csvData = []


def spamUpdate(tweet_id, spam, clear_text, training):
    Database.unTweeterizeTable.update_item(
        Key={'tweet_id': tweet_id},
        UpdateExpression="set is_spam=:s, clear_text=:c, is_training=:t",
        ExpressionAttributeValues={
            ':s': spam,
            ':c': clear_text,
            ':t': training
        },
        ReturnValues="UPDATED_NEW"
    )

with open('test.csv', 'rb') as f:
    reader = csv.DictReader(f)
    for row in reader:
        tweet_id = row["tweet_id"].strip()

        spam = False

        if row["SPAM"].strip() == 'x':
            spam = True

        # print("id: {} - s: {} | i: {}".format(tweet_id, spam))
        csvData.append((tweet_id, spam))


allTweets = Database.getAll(Database.unTweeterizeTable)


def remove_user(userTweet):
    userTweet = re.sub('@[^\s]+', 'AT_USER', userTweet)
    return userTweet


for tweet in allTweets:

    tweetCsv = filter(lambda x: x[0] == tweet["tweet_id"], csvData)

    if len(tweetCsv) == 1:
        tweet["is_spam"] = tweetCsv[0][1]
        tweet["clear_text"] = remove_user(tweet["clear_text"])
        tweet["is_training"] = True

        spamUpdate(tweet["tweet_id"], tweet["is_spam"], tweet["clear_text"], tweet["is_training"])

print("\n\nACABOU!!!\n\n")