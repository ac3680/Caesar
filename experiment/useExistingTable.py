import boto3
from boto3.dynamodb.conditions import Key, Attr

# Get the service resource.
dynamodb = boto3.resource('dynamodb')

# Instantiate a table resource object without actually
# creating a DynamoDB table. Note that the attributes of this table
# are lazy-loaded: a request is not made nor are the attribute
# values populated until the attributes
# on the table resource are accessed or its load() method is called.
table = dynamodb.Table('users')

# Create item
table.put_item(
    Item={
        'username': 'blanks',
        'first_name': 'Nina',
        'last_name': 'B'
    }
)

# Get item
def get_item():
    response = table.get_item(
        Key={
            'username': 'blanks',
            'last_name': 'B'
        }
    )
    item = response['Item']
    print(item)
    return item

item = get_item()

# Update item with nonexisting field
item['age'] = 25
table.put_item(Item=item)

get_item()

# Update item existing field
item['age'] = 26
table.put_item(Item=item)

get_item()

everyone_else = [
    {
    'username': 'hippo',
    'first_name': 'Agustin',
    'last_name': 'C',
    'age': 8
    },
    {
    'username': 'bluemelodia',
    'first_name': 'Melanie',
    'last_name': 'H',
    'age': 9
    },
    {
    'username': 'houston',
    'first_name': 'Whitney',
    'last_name': 'B',
    'age': 10
    }
]

# Batch write
with table.batch_writer() as batch:
    for someone in everyone_else:
        batch.put_item(Item=someone)


# Query one person
response = table.query(
    KeyConditionExpression=Key('username').eq('bluemelodia')
)
items = response['Items']
print(items)

# Scan for a condition
response = table.scan(
    FilterExpression=Attr('age').lt(27)
)
items = response['Items']
print(items)
