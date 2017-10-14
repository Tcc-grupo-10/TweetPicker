import csv
from Databases import Database

csvData = []

with open('test.csv', 'rb') as f:
    reader = csv.DictReader(f)
    for row in reader:
        tweet_id = row["tweet_id"].strip()

        spam = False
        irrelevante = False

        if row["SPAM"].strip() == 'x':
            spam = True

        if row["IRRELEVANTE"].strip():
            irrelevante = True

        print "id: {} - s: {} | i: {}".format(tweet_id, spam, irrelevante)
        csvData.append((tweet_id, spam, irrelevante))


allTweets = Database.getAll(Database.unTweeterizeTable)

for tweet in allTweets:

    tweet["training_tweet"] = True
    tweetCsv = filter(lambda x: x[0] == tweet["tweet_id"], csvData)

    if len(tweetCsv) == 1:
        tweet["is_spam"] = tweetCsv[1]
        tweet["is_irrelevant"] = tweetCsv[2]

    # TODO -> Update unTweeterizeTable





