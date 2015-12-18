import json
import time
import boto.sqs
from boto.sqs.message import RawMessage
while True:
    keys = [line.rstrip('\n\r') for line in open('keys.txt')]

    #DO A GET --------------------------------------------------------------------------------
    jsonobj = json.dumps(
                            {
                                "req": [
                                    {
                                        "op": "GET",
                                        "target": "/K12",
                                        "respQ": "CliQ",
                                        "corrID": "864"
                                    }
                                ]
                            }
                        )

    conf = {
      "sqs-access-key": keys[0],
      "sqs-secret-key": keys[1],
      "sqs-queue-name": "K12",
      "sqs-region": "us-west-2",
      "sqs-path": "sqssend"
    }

    conn = boto.sqs.connect_to_region(
            conf.get('sqs-region'),
            aws_access_key_id = conf.get('sqs-access-key'),
            aws_secret_access_key = conf.get('sqs-secret-key')
    )

    q = conn.create_queue(conf.get('sqs-queue-name'))

    m = RawMessage()
    m.set_body(jsonobj)
    retval = q.write(m)
    print 'added message, got retval: %s' % retval
    
    time.sleep(5)