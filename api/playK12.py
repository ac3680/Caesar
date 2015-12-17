import datetime
import pprint
import requests
import sys

from bson.json_util import dumps

# Import and initialize Flask
from flask import Flask, url_for
from flask import request
from flask import json
from flask import Response
from flask import jsonify
app = Flask(__name__)

# Globals
GET = 'GET'
POST = 'POST'
PUT = 'PUT'
DELETE = 'DELETE'

@app.route('/K12', methods = [GET])
def get():
    return "GET"

@app.route('/K12', methods = [POST])
def post():
    return "POST"
    
@app.route('/K12', methods = [PUT])
def put():
    return "PUT"
    
@app.route('/K12', methods = [DELETE])
def delete():
    return "DELETE"

if __name__ == '__main__':
    app.run(
        debug = True,
        port = 1235
    )
