import requests
import boto3
import re
from boto3.dynamodb.conditions import Key, Attr
from bson.json_util import dumps
from boto3.session import Session
from flask import Flask, url_for
from flask import request
from flask import json
from flask import Response
from flask import jsonify
from SecurityService import encrypt

SECURITY_TOGGLE_ON = False

# Read AWS account keys from file
keys = [line.rstrip('\n\r') for line in open('keys.txt')]
session = Session(aws_access_key_id=keys[0],
                  aws_secret_access_key=keys[1],
                  region_name='us-east-1')

# Set up Dynamo
dynamodb = session.resource('dynamodb')
table = dynamodb.Table('students')

# Set up Flask
app = Flask(__name__)
app.config['DYNAMO_TABLES'] = [table]

#==============================================================================
# Database Operations: (C)reate, (R)ead, (U)pdate, (D)elete
#==============================================================================

# Create - Capable of overwrite
def create_item(student):
    table.put_item(
        Item=student
    )
    return student

# Read
def find_item(uid):
    response = table.get_item(
        Key={ 'uid': uid }
    )
    return response['Item'] if 'Item' in response else None

def find_all_items():
    response = table.scan()
    return response['Items'] if 'Items' in response else []

# Update - Reads first, then re-Creates
def update_item(uid, new_student_data):
    student = find_item(uid)
    if student:
        for (key, value) in new_student_data.iteritems():
            student[key] = value
        create_item(student)
        return student
    else:
        return None

# Delete
def delete_item(uid):
    table.delete_item(
    Key={ 'uid': uid }
    )

# Update - as a batch
def batch_update(students):
    with table.batch_writer() as batch:
        for student in students:
            batch.put_item(Item=student)

#==============================================================================
# REST Operations
#==============================================================================

# POST .../students - Create a new student
@app.route('/k12', methods = ['POST'])
def post_student():
    data = form_or_json()
    student = {key: value for (key, value) in data.iteritems()}

    if SECURITY_TOGGLE_ON and not valid_signature(student):
        return unauthorized()

    if 'uid' not in student:
        return unprocessable_entity("need uid to create new student")
    for key, value in student.iteritems():
        student[key] = sanitize(value)
        if (student[key] == ''):
            return bad_request("improper UID format")
    uid = student['uid']
    if find_item(uid):
        return unprocessable_entity("the entity already exists")
    create_item(student)
    return "OK: new student(" + uid + ") created\n", 201

# GET .../students/<uid> - Get a student by uid
@app.route('/k12/<uid>', methods = ['GET'])
def get_student(uid):
    if SECURITY_TOGGLE_ON and not valid_signature():
        return unauthorized()
    uid = sanitize(uid)
    if (uid == ''):
        return bad_request("improper UID format")
    student = find_item(uid)
    if student:
        return dumps(student), 200
    else:
        return not_found()

# GET .../students - Get all students
@app.route('/k12', methods = ['GET'])
def get_all_students():
    if SECURITY_TOGGLE_ON and not valid_signature():
        return unauthorized()

    students = find_all_items()
    if students:
        return dumps(students), 200
    else:
        return not_found()

# PUT .../students/<uid> - Update student field
@app.route('/k12/<uid>', methods=['PUT'])
def update_student(uid):
    data = form_or_json()
    student = {key: value for (key, value) in data.iteritems()}

    if SECURITY_TOGGLE_ON and not valid_signature(student):
        return unauthorized()

    if 'uid' in student:
        return unprocessable_entity("modifying the uid field is forbidden")
    for key, value in student.iteritems():
        student[key] = sanitize(value)
        if (student[key] == ''):
            return bad_request("improper UID format")
    new_student = update_item(uid, student)
    if new_student:
        return "OK: student(" + uid + ") updated successfully\n", 200
    else:
        return not_found()

# DELETE .../students/<uid> - Delete a student
@app.route('/k12/<uid>', methods=['DELETE'])
def delete_student(uid):
    if SECURITY_TOGGLE_ON and not valid_signature():
        return unauthorized()

    uid = sanitize(uid)
    if (uid == ''):
        return bad_request("improper UID format")
    student = find_item(uid)
    if student:
        delete_item(uid)
        return "No Content: student(" + uid + ") deleted successfully\n", 204
    else:
        return not_found()

#==============================================================================
# Schema Changes
#==============================================================================

# PUT .../k12/schema/table - Add a column to the table schema with default values
@app.route('/k12/schema/table', methods = ['PUT'])
def update_schema():
    data = form_or_json()
    students = find_all_items()
    for student in students:
        for (key, value) in data.iteritems():
            if key == 'uid':
                return unprocessable_entity("modifying the uid field is forbidden")
            student[key] = sanitize(value)
            if (student[key] == ''):
                return bad_request("improper UID format")
    batch_update(students)
    return "OK: schema successfully updated\n", 200

# DELETE .../k12/schema/table/<key> - Delete a column from the table schema
@app.route('/k12/schema/table/<key>', methods = ['DELETE'])
def delete_schema(key):
    key = sanitize(key)
    if key == '':
        return bad_request("improper UID format")
    if key == 'uid':
        return unprocessable_entity("deleting the uid field is forbidden")
    students = find_all_items()
    for student in students:
        uid = student['uid']
        try:
            del student[key]
        except KeyError:
            pass
    batch_update(students)
    return "No Content: schema key(" + key + ") successfully deleted\n", 204

#==============================================================================
# Error Handling
#==============================================================================

# Handle nonexistent routes
@app.errorhandler(404)
def not_found(error=None):
    message = {
            'status': 404,
            'message': 'Not Found: ' + request.url,
    }
    response = jsonify(message)
    response.status_code = 404
    return response

@app.errorhandler(400)
def bad_request(detail, error=None):
    message = {
            'status': 400,
            'message': 'Bad Request: ' + detail
    }
    response = jsonify(message)
    response.status_code = 400
    return response

@app.errorhandler(401)
def unauthorized(error=None):
    message = {
            'status': 401,
            'message': 'Unauthorized Transaction'
    }
    response = jsonify(message)
    response.status_code = 401
    return response

@app.errorhandler(422)
def unprocessable_entity(detail, error=None):
    message = {
            'status': 422,
            'message': 'Unprocessable Entity: ' + detail
    }
    response = jsonify(message)
    response.status_code = 422
    return response

#==============================================================================
# Helper Methods
#==============================================================================

# Returns data whether from request.form or request.data
def form_or_json():
    data = request.data
    return json.loads(data) if data is not '' else request.form

# Code injection defense
def sanitize(value):
    try:
        if value.isalnum():
            return value
        else:
            return ''
    except:
        return ''
    # Convert empty values to a space
    if len(value) < 1:
        return ' '
    return value

# Check signature
def valid_signature(student=None):
    signature = request.headers.get('signature')
    if not signature:
        return False
    # Get the type of request and URI ex. GET /k12/nb2406
    message = request.method + ' ' + request.script_root + request.path
    if student:
        for (key, value) in student.iteritems():
            message = message + " " + str(value)
    hash_value = encrypt(message)
    if hash_value != int(signature):
        return False
    return True

if __name__ == '__main__':
    app.run(
        port = 9002
    )
