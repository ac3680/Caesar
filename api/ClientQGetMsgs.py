import json
import time
import boto.sqs
from boto.sqs.message import RawMessage
while True:
    keys = [line.rstrip('\n\r') for line in open('keys.txt')]

    conf = {
      "sqs-access-key": keys[0],
      "sqs-secret-key": keys[1],
      "sqs-queue-name": "CliQ",
      "sqs-region": "us-west-2",
      "sqs-path": "sqssend"
    }

    conn = boto.sqs.connect_to_region(
            conf.get('sqs-region'),
            aws_access_key_id = conf.get('sqs-access-key'),
            aws_secret_access_key = conf.get('sqs-secret-key')
    )

    q = conn.create_queue(conf.get('sqs-queue-name'))

    for m in q.get_messages():
        print '%s: %s' % (m, m.get_body())
        q.delete_message(m)