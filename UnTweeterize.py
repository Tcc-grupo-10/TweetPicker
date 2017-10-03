import boto3
import os
import Database
import DatabaseCreator
import re
from unidecode import unidecode


def processTweet(tweet):
    #TODO -> emoji to text HERE

    #To unicode
    tweet = unidecode(tweet)
    tweet = unicode(tweet)

    #Convert to lower case
    tweet = tweet.lower()
    #Convert www.* or https?://* to URL
    tweet = re.sub('((www\.[^\s]+)|(https?://[^\s]+))', '', tweet)
    #Removing \n
    tweet = tweet.replace('\n', ' ')
    #Remove additional white spaces
    tweet = re.sub('[\s]+', ' ', tweet)
    #Replace #word with word
    tweet = re.sub(r'#([^\s]+)', r'\1', tweet)
    #trim
    tweet = tweet.strip('\'"')

    tweet = tweet.replace('[?]', '')
    tweet = tweet.replace('&amp;', '&')
    tweet = tweet.replace('&lt;', '<')
    tweet = tweet.replace('&gt;', '>')

    return tweet


# Script \/


accessKey = os.environ['access_key']
secretAccess = os.environ['secret_access']

# Get the service resource.
dynamodb = boto3.resource('dynamodb', region_name='sa-east-1', aws_access_key_id=accessKey, aws_secret_access_key=secretAccess)
tweetRTTable = DatabaseCreator.tweetRTTable(dynamodb)

response = tweetRTTable.scan()
allTweets = response['Items']

print len(allTweets)

"""while 'LastEvaluatedKey' in response:
    response = boto3.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
    allTweets.extend(response['Items'])
    print len(allTweets)"""

for i in allTweets:
    print i
    i["text"] = processTweet(i["text"])
    print i
    print i["text"]
    print "\n\n"
