import boto3
from boto3.session import Session

# Read AWS account keys from file
keys = [line.rstrip('\n\r') for line in open('keys.txt')]
session = Session(aws_access_key_id=keys[0],
                  aws_secret_access_key=keys[1],
                  region_name='us-east-1')

# Set up Dynamo
dynamodb = session.resource('dynamodb')

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
