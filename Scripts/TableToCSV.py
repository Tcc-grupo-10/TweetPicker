import csv
from Databases import Database

allTweets = Database.getAll(Database.unTweeterizeTable)

f = csv.writer(open("Etc/test.csv", "wb+"))
f.writerow(["tweet_id", "search_key", "clear_text", "SPAM", "IRRELEVANTE"])
for x in allTweets:
    f.writerow([x["tweet_id"],
                x["search_key"],
                x["clear_text"]])
