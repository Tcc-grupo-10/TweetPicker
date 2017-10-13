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
                'WriteCapacityUnits': 5
            }
        )

        # Wait until the table exists.
        table.meta.client.get_waiter('table_exists').wait(TableName=tableName)

        return table

def tweetRTTable(dynamodb):
    tableName = 'RTCleanV2'

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
                'WriteCapacityUnits': 5
            }
        )

        # Wait until the table exists.
        table.meta.client.get_waiter('table_exists').wait(TableName=tableName)

        return table

def unTweeterizeTable(dynamodb):
    tableName = 'UnTweeterize'

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
                'WriteCapacityUnits': 5
            }
        )

        # Wait until the table exists.
        table.meta.client.get_waiter('table_exists').wait(TableName=tableName)

        return table
