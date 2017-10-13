import boto3
import os
import Database
import DatabaseCreator


accessKey = os.environ['access_key']
secretAccess = os.environ['secret_access']

# Get the service resource.
dynamodb = boto3.resource('dynamodb', region_name='sa-east-1', aws_access_key_id=accessKey, aws_secret_access_key=secretAccess)
tweetsTable = DatabaseCreator.tweetTable(dynamodb)
tweetsRTClean = DatabaseCreator.tweetRTTable(dynamodb)

response = tweetsTable.scan()
allTweets = response['Items']

print len(allTweets)

while 'LastEvaluatedKey' in response:
    response = tweetsTable.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
    allTweets.extend(response['Items'])
    print len(allTweets)

isRt = 0
notRt = 0

for i in allTweets:
    if "RT " in i["text"]:
        isRt = isRt + 1
        print "\nIS Retweet: {} | ".format(isRt) + i["text"]
    else:
        notRt = notRt + 1
        print "\nNOT Retweet: {} | ".format(notRt) + i["text"]
        Database.insertItem(i, tweetsRTClean)


print "\n\n"
print isRt
print "\n\n"
print notRt