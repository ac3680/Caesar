'''
@app.route('/k12', methods = ['POST'])
@app.route('/k12/<uid>', methods = ['GET'])
@app.route('/k12', methods = ['GET'])
@app.route('/k12/<uid>', methods=['PUT'])
@app.route('/k12/<uid>', methods=['DELETE'])
@app.route('/k12/schema/table', methods = ['PUT'])
@app.route('/k12/schema/table/<key>', methods = ['DELETE'])
'''
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
                                        "target": "/k12",
                                        "respQ": "CliQ",
                                        "corrID": "861"
                                    }
                                ],
                                "body": [
                                    {
                                        'uid': 'newuser1',
                                        'first_name': 'user',
                                        'last_name': 'ln',
                                        'school': 'SCE'
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
    
    time.sleep(1)

    #DO A GET --------------------------------------------------------------------------------
    jsonobj = json.dumps(
                            {
                                "req": [
                                    {
                                        "op": "GET",
                                        "target": "/k12/newuser1",
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
    
    time.sleep(1)

    #DO A GET --------------------------------------------------------------------------------
    jsonobj = json.dumps(
                            {
                                "req": [
                                    {
                                        "op": "GET",
                                        "target": "/k12",
                                        "respQ": "CliQ",
                                        "corrID": "8687"
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
    
    time.sleep(1)
    
    #DO A PUT --------------------------------------------------------------------------------
    jsonobj = json.dumps(
                            {
                                "req": [
                                    {
                                        "op": "PUT",
                                        "target": "/k12/newuser1",
                                        "respQ": "CliQ",
                                        "corrID": "862"
                                    }
                                ],
                                "body": [
                                    {
                                        'first_name': 'user2',
                                        'last_name': 'ln2',
                                        'school': 'SCE2'
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
    
    time.sleep(1)    
    
    
    #DO A DELETE --------------------------------------------------------------------------------
    jsonobj = json.dumps(
                            {
                                "req": [
                                    {
                                        "op": "DELETE",
                                        "target": "/k12/newuser1",
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
    
    time.sleep(500)    
    
    
    #DO A PUT --------------------------------------------------------------------------------
    jsonobj = json.dumps(
                            {
                                "req": [
                                    {
                                        "op": "PUT",
                                        "target": "/k12/schema/table",
                                        "respQ": "CliQ",
                                        "corrID": "8652"
                                    }
                                ],
                                "body": [
                                    {
                                        'new_field': 'Null'
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
    
    time.sleep(500)
    
    
    #DO A DELETE --------------------------------------------------------------------------------
    jsonobj = json.dumps(
                            {
                                "req": [
                                    {
                                        "op": "DELETE",
                                        "target": "/k12/schema/table/new_field",
                                        "respQ": "CliQ",
                                        "corrID": "869"
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