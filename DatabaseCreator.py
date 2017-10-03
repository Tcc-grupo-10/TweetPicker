def tweetTable(dynamodb):
    tableName = 'tweets15'

    try:
        dynamodb.Table(tableName).creation_date_time
        return dynamodb.Table(tableName)

    except Exception:
        table = dynamodb.create_table(
            TableName=tableName,
            KeySchema=[
                {
                    'AttributeName': 'tweet_id',
                    'KeyType': 'HASH'
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'tweet_id',
                    'AttributeType': 'S'
                },
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 15
            }
        )

        # Wait until the table exists.
        table.meta.client.get_waiter('table_exists').wait(TableName='tweets15')

        return table
