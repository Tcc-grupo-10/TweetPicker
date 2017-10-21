import os
import Databases

accessKey = os.environ['access_key']
secretAccess = os.environ['secret_access']

response = Databases.Database.tweetsTable.scan()
allTweets = response['Items']

print (len(allTweets))

while 'LastEvaluatedKey' in response:
    response = Databases.Database.tweetsTable.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
    allTweets.extend(response['Items'])
    print (len(allTweets))

isRt = 0
notRt = 0

for tweet in allTweets:
    if "RT " in tweet["text"]:
        isRt = isRt + 1
        print ("\nIS Retweet: {} | ".format(isRt) + tweet["text"])
    else:
        notRt = notRt + 1
        print ("\nNOT Retweet: {} | ".format(notRt) + tweet["text"])
        Databases.insertItem(tweet, Databases.Database.tweetRTTable)


print ("\n\n")
print (isRt)
print ("\n\n")
print (notRt)