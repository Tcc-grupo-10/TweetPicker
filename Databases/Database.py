import os
import boto3
from Databases import DatabaseCreator

accessKey = os.environ['access_key']
secretAccess = os.environ['secret_access']

# Get the service resource.
dynamodb = boto3.resource('dynamodb', region_name='sa-east-1', aws_access_key_id=accessKey, aws_secret_access_key=secretAccess)

# TRAINING STUFF
tweetTable = DatabaseCreator.tweetTable(dynamodb)
tweetRTTable = DatabaseCreator.tweetRTTable(dynamodb)
unTweeterizeTable = DatabaseCreator.unTweeterizeTable(dynamodb)

# JUST USERS CAN USE IT!!!
rawTweets = DatabaseCreator.rawTweets(dynamodb)


def insertItem(item, table):
    try:
        table.put_item(Item = item)
    except Exception as e:
        print ("ERRO INSERINDO: ({0}): {1}".format(e.errno, e.strerror))


def updateItem(item, table):
    # TODO -> JUST DO IT!
    try:
        # table.put_item(Item=item)
        print ("If you are reading this on the console, you forgot to do the Database.updateItem")
    except Exception as e:
        print ("ERRO INSERINDO: ({0}): {1}".format(e.errno, e.strerror))


def countItens(table):
    print (table.item_count)


def getAll(table):
    response = table.scan()
    allTweets = response['Items']
    print (len(allTweets))

    """while 'LastEvaluatedKey' in response:
        response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
        allTweets.extend(response['Items'])
        print len(allTweets)"""

    return allTweets


def deleteItem(tweet_id, table):
    table.delete_item(Key={"tweet_id": tweet_id})
