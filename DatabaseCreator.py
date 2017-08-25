def tweetTable(dynamodb):
    tableName = 'tweets'

    try:
        print "<< -- TRYING -- >> "
        dynamodb.Table(tableName).creation_date_time
        return dynamodb.Table(tableName)

    except Exception, e:
        print '<< -- FAIL -->>  ' + str(e)
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
        table.meta.client.get_waiter('table_exists').wait(TableName='tweets')

        return table
