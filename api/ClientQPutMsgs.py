import json
import time
import boto.sqs
from boto.sqs.message import RawMessage
while True:
    keys = [line.rstrip('\n\r') for line in open('keys.txt')]

    #DO A POST --------------------------------------------------------------------------------
    jsonobj = json.dumps(
                            {
                                "req": [
                                    {
                                        "op": "POST",
                                        "target": "/K12",
                                        "respQ": "CliQ",
                                        "corrID": "861"
                                    }
                                ],
                                "body": [
                                    {
                                        "header": "Belmont",
                                        "longitude": "-71.4594",
                                        "post code": "02178",
                                        "latitude": "42.4464"
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

    
    #DO A PUT --------------------------------------------------------------------------------
    jsonobj = json.dumps(
                            {
                                "req": [
                                    {
                                        "op": "PUT",
                                        "target": "/K12",
                                        "respQ": "CliQ",
                                        "corrID": "862"
                                    }
                                ],
                                "body": [
                                    {
                                        "header": "Belmont",
                                        "longitude": "-71.4594",
                                        "post code": "02178",
                                        "latitude": "42.4464"
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
    
    
    #DO A DELETE --------------------------------------------------------------------------------
    jsonobj = json.dumps(
                            {
                                "req": [
                                    {
                                        "op": "DELETE",
                                        "target": "/K12",
                                        "respQ": "CliQ",
                                        "corrID": "863"
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