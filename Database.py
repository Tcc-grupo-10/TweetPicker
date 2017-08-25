import boto3
import DatabaseCreator
import os


accessKey = os.environ['access_key']
secretAccess = os.environ['secret_access']

print "access " + accessKey
print "secretAccess " + secretAccess

# Get the service resource.
dynamodb = boto3.resource('dynamodb', region_name='sa-east-1', aws_access_key_id=accessKey, aws_secret_access_key=secretAccess)

tweetTable = DatabaseCreator.tweetTable(dynamodb)

def insertItem(item):
    tweetTable.put_item(Item = item)


def countItens():
    print tweetTable.item_count