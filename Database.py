import boto3
import DatabaseCreator

# Get the service resource.
dynamodb = boto3.resource('dynamodb', endpoint_url='http://localhost:8000', region_name='us-west-2', aws_access_key_id='foo', aws_secret_access_key='foo')

tweetTable = DatabaseCreator.tweetTable(dynamodb)
print(tweetTable.item_count)