import os
import boto3


class DatabaseConnector(object):
    def __init__(self, table_name="Tweets"):
        self._access_key = os.environ['access_key']
        self._secret_access_key = os.environ['secret_access']
        self.table_name = table_name
        self._dynamodb_client = boto3.resource('dynamodb',
                                               region_name='sa-east-1',
                                               aws_access_key_id=self._access_key,
                                               aws_secret_access_key=self._secret_access_key)
        self._table = self._dynamodb_client.Table(self.table_name)

    def insert_tweet(self, tweet):
        self._table.put_item(
            Item={
                'runID': tweet.run_id,
                'tweetID': tweet.id,
                'original_text': tweet.original_tweet,
                'retweet_count': tweet.number_of_rts,
                'favorite_count': tweet.number_of_favorites,
                'author_id': tweet.author_id,
                'created_at': tweet.created_at,
                'language': tweet.language,
                'search_key': tweet.search_key
            }
        )

    def save_preprocessed_tweet(self, tweet):
        self._table.update_item(
            Key={
                'runID': tweet.run_id,
                'tweetID': tweet.id,
            },
            UpdateExpression="set preprocessed_tweet = :r ",
            ExpressionAttributeValues={':r': tweet.preprocessed_tweet}
        )

        self._table.update_item(
            Key={
                'runID': tweet.run_id,
                'tweetID': tweet.id,
            },
            UpdateExpression="set emoji = :r ",
            ExpressionAttributeValues={':r':  tweet.emojis}
        )

    def save_formatted_tweet(self, tweet):
        self._table.update_item(
            Key={
                'runID': tweet.run_id,
                'tweetID': tweet.id,
            },
            UpdateExpression="set formatted_tweet = :r ",
            ExpressionAttributeValues={':r': tweet.formatted_tweet}
        )

    def get_all(self):
        response = self._table.scan()
        allTweets = response['Items']
        print(len(allTweets))

        while 'LastEvaluatedKey' in response:
            response = self._table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
            allTweets.extend(response['Items'])
            print(len(allTweets))

        return allTweets


