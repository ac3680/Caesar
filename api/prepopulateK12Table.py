import boto3
from boto3.session import Session

# Read AWS account keys from file
keys = [line.rstrip('\n') for line in open('keys.txt')]
session = Session(aws_access_key_id=keys[0],
                  aws_secret_access_key=keys[1],
                  region_name='us-east-1')

# Set up Dynamo
dynamodb = session.resource('dynamodb')

# Get the service resource.
# dynamodb = boto3.resource('dynamodb')

table = dynamodb.Table('students')

team_motley = [
    {
    'uid': 'nb2406',
    'first_name': 'Nina',
    'last_name': 'B',
    'school': 'SCE'
    },
    {
    'uid': 'ac3680',
    'first_name': 'Agustin',
    'last_name': 'C',
    'school': 'GS'
    },
    {
    'uid': 'mlh2197',
    'first_name': 'Melanie',
    'last_name': 'H',
    'school': 'SEAS'
    },
    {
    'uid': 'wvb2103',
    'first_name': 'Whitney',
    'last_name': 'B',
    'school': 'SEAS'
    }
]

# Batch write
with table.batch_writer() as batch:
    for member in team_motley:
        batch.put_item(Item=member)
