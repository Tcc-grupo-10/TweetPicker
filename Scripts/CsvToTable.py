import csv

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
