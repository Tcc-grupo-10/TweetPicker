import csv
import os

import boto3

from Databases import DatabaseCreator

accessKey = os.environ['access_key']
secretAccess = os.environ['secret_access']

# Get the service resource.
dynamodb = boto3.resource('dynamodb', region_name='sa-east-1', aws_access_key_id=accessKey, aws_secret_access_key=secretAccess)
unTweeterizeTable = DatabaseCreator.unTweeterizeTable(dynamodb)

response = unTweeterizeTable.scan()
allTweets = response['Items']
print len(allTweets)

while 'LastEvaluatedKey' in response:
    response = unTweeterizeTable.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
    allTweets.extend(response['Items'])
    print len(allTweets)

f = csv.writer(open("test.csv", "wb+"))
f.writerow(["tweet_id", "search_key", "retweet_count", "favorite_count", "user_id", "text", "SPAM", "IRRELEVANTE"])
for x in allTweets:
    f.writerow([x["tweet_id"],
                x["search_key"],
                x["retweet_count"],
                x["favorite_count"],
                x["user_id"],
                x["text"]])
