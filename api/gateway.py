# Turns SQS into request to K12/Other queue, and returns response to the client queue, "CliQ"

# -------------------- Imports and Initializations -------------------->

from flask import Flask
from flask import Response
from flask import stream_with_context
from flask import request

from werkzeug.routing import BaseConverter

import requests
import json
import pickle
import time
import boto.sqs
from boto.sqs.message import RawMessage
import pdb

app = Flask(__name__)

class RegexConverter(BaseConverter):
    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]
                
app.url_map.converters['regex'] = RegexConverter
   
# Read AWS account keys from file
keys = [line.rstrip('\n') for line in open('keys.txt')]

# Find the list of queue names and routes that we are dealing with
queues = [line.rstrip('\n') for line in open('config.txt')]
qList = []
for each in queues:
    qList.append(each.split(','))

# <----------------- End of Imports and Initializations -----------------

# ---------------------- Functions and Execution ----------------------->

# Function to put response object into client queue
def putInQueue(responseObj, responseQueue):
    print "putting in client queue"
    conf = {
      "sqs-access-key": keys[0],
      "sqs-secret-key": keys[1],
      "sqs-queue-name": responseQueue,
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
    m.set_body(responseObj)
    retval = q.write(m)
    print 'added message, got retval: %s' % retval
    return 0

# For each queue in our config.txt file, loop forever, drawing messages from each one
# and directing them to the route specified in the corresponding config.txt route
while True:
    for route in qList:
        print "Now reading this queue:", route[0]

        # Prepare SQS retrieval, connect, and retrieve
        conf = {
          "sqs-access-key": keys[0],
          "sqs-secret-key": keys[1],
          "sqs-queue-name": route[0],
          "sqs-region": "us-west-2",
          "sqs-path": "sqssend"
        }

        conn = boto.sqs.connect_to_region(
                conf.get('sqs-region'),
                aws_access_key_id = conf.get('sqs-access-key'),
                aws_secret_access_key = conf.get('sqs-secret-key')
        )

        q = conn.create_queue(conf.get('sqs-queue-name')) #re-creates the queue if necessary, does not overwrite it
        
        # For each message in the queue
        for m in q.get_messages():
            print '%s: %s' % (m, m.get_body())
            q.delete_message(m)
            
            requestIn = json.loads(m.get_body())
            targetURL = route[1] + requestIn['req'][0]['target']
            
            # Request in SQS Queue is GET, send synchronously to K12 and put response into client queue
            if requestIn['req'][0]['op'] == 'GET':
                print 'we are doing a get on', targetURL
                req = requests.get(targetURL, stream = True)
                responseObj = json.dumps({"response":[{"body": req.text,"status": req.status_code}],"corrID": requestIn['req'][0]['corrID']})
                putInQueue(responseObj, requestIn['req'][0]['respQ'])
                
            # Request in SQS Queue is POST, send synchronously to K12 and put response into client queue
            if requestIn['req'][0]['op'] == 'POST':
                data = {}
                for k,v in requestIn['body'][0].iteritems():
                    data.update({k:v})
                req = requests.post(targetURL, data=data)
                responseObj = json.dumps({"response":[{"body": req.text,"status": req.status_code}],"corrID": requestIn['req'][0]['corrID']})
                putInQueue(responseObj, requestIn['req'][0]['respQ'])
                
            # Request in SQS Queue is PUT, send synchronously to K12 and put response into client queue
            if requestIn['req'][0]['op'] == 'PUT':
                data = {}
                for k,v in requestIn['body'][0].iteritems():
                    data.update({k:v})
                req = requests.put(targetURL, data=data)
                responseObj = json.dumps({"response":[{"body": req.text,"status": req.status_code}],"corrID": requestIn['req'][0]['corrID']})
                putInQueue(responseObj, requestIn['req'][0]['respQ'])
                
            # Request in SQS Queue is DELETE, send synchronously to K12 and put response into client queue
            if requestIn['req'][0]['op'] == 'DELETE':
                req = requests.delete(targetURL, stream = True)
                responseObj = json.dumps({"response":[{"body": req.text,"status": req.status_code}],"corrID": requestIn['req'][0]['corrID']})
                putInQueue(responseObj, requestIn['req'][0]['respQ'])
                
# <-------------------- End of Functions and Execution --------------------