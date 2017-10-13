import boto3
import os
import json


accessKey = os.environ['access_key']
secretAccess = os.environ['secret_access']

# Get the service resource.
dynamodb = boto3.resource('dynamodb', region_name='sa-east-1', aws_access_key_id=accessKey, aws_secret_access_key=secretAccess)

#sourceTable = dynamodb.Table('tweets')
sourceTable = dynamodb.Table('tweetsBig')
destinyTable = dynamodb.Table('tweets15')

response = sourceTable.scan()
allTweets = response['Items']

print len(allTweets)

while 'LastEvaluatedKey' in response:
    response = sourceTable.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
    allTweets.extend(response['Items'])
    print len(allTweets)


for i in allTweets:
    try:
        destinyTable.put_item(Item=i)
        print(i)
    except Exception as e:
        print "I/O error({0}): {1}".format(e.errno, e.strerror)