import boto3

# Get the service resource.
dynamodb = boto3.resource('dynamodb')

# Create the DynamoDB table.
# A second index can be included of KeyType 'RANGE'
table = dynamodb.create_table(
    TableName='students',
    KeySchema=[
        {
            'AttributeName': 'uid',
            'KeyType': 'HASH'
        }
    ],
    AttributeDefinitions=[
        {
            'AttributeName': 'uid',
            'AttributeType': 'S'
        }
    ],
    ProvisionedThroughput={
        'ReadCapacityUnits': 50,
        'WriteCapacityUnits': 50
    }
)

# Wait until the table exists.
table.meta.client.get_waiter('table_exists').wait(TableName='users')

# Print out some data about the table. Should return 0.
print(table.item_count)
