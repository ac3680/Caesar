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
@app.route('/K12', methods = ['POST'])
def post_student():
    data = form_or_json()
    student = {key: value for (key, value) in data.iteritems()}
    #print "Student: " + str(student)
    if 'uid' not in student:
        return "Need uid to create new student\n", 400
    #print "UID: " + str(student['uid'])
    for key, value in student.iteritems():
	#print key + " " + value
   	try:
            regex = re.compile('[^0-9a-zA-Z]')
	    if (key == 'uid'):
		#print "uid: " + key
     		uid = regex.sub('', str(student['uid']))
	    else:
		#print key
	        student[key] = regex.sub('', str(student[key]))
		if len(student[key]) < 1:
	    	    message = "Bad request, improper " + key + " format"
	    	    return message, 400
        except:
	    message = "Bad request, improper " + key + " format"
            return message, 400
    if len(uid) < 1:
        return "Bad request, improper uid format", 400
    if find_item(uid):
        return "The student(" + uid + ") already exists", 422
    create_item(student)
    message = "New student(" + uid+ ") created\n"
    return message, 201

# GET .../students/<uid> - Get a student by uid
@app.route('/K12/<uid>', methods = ['GET'])
def get_student(uid):
    try:
        regex = re.compile('[^0-9a-zA-Z]')
        uid = regex.sub('', uid)
    except:
	return "Bad request, improper UID format", 400
    if len(uid) < 1:
	return "Bad request, improper UID format", 400
    student = find_item(uid)
    if student:
        return dumps(student), 200
    else:
        return not_found()

# GET .../students - Get all students
@app.route('/K12', methods = ['GET'])
def get_all_students():
    students = find_all_items()
    if students:
        return dumps(students), 200
    else:
        return not_found()

# PUT .../students/<uid> - Update student field
@app.route('/K12/<uid>', methods=['PUT'])
def update_student(uid):
    data = form_or_json()
    student = {key: value for (key, value) in data.iteritems()}
    if 'uid' in student:
        return "Updating a student's uid is forbidden\n", 422
    for key, value in student.iteritems():
   	try:
            regex = re.compile('[^0-9a-zA-Z]')
	    student[key] = regex.sub('', str(student[key]))
	    if len(student[key]) < 1:
	    	message = "Bad request, improper " + key + " format"
		return message, 400
        except:
	    message = "Bad request, improper " + key + " format"
            return message, 400
    new_student = update_item(uid, student)
    if new_student:
        return "Student(" + uid + ") updated successfully", 200
    else:
        return not_found()

# DELETE .../students/<uid> - Delete a student
@app.route('/K12/<uid>', methods=['DELETE'])
def delete_student(uid):
    try:
        regex = re.compile('[^0-9a-zA-Z]')
        uid = regex.sub('', uid)
    except:
        return "Bad request, improper UID format", 400
    if len(uid) < 1:
	return "Bad request, improper UID format", 400
    student = find_item(uid)
    if student:
        delete_item(uid)
        return "Student(" + uid + ") deleted successfully", 200
    else:
        return not_found()

#==============================================================================
# Schema Changes
#==============================================================================

# PUT .../K12/schema/table - Add a column to the table schema with default values
@app.route('/K12/schema/table', methods = ['PUT'])
def update_schema():
    try:
        data = form_or_json()
        students = find_all_items()
        for student in students:
            uid = student['uid']
            for (key, value) in data.iteritems():
                if key == 'uid':
                try: 
                    return "Modifying a student's uid field is forbidden\n", 422
		    regex = re.compile('[^0-9a-zA-Z]')
		    value = regex.sub('', value)
		except: 
		    message = "Bad request, improper " + str(key) + " format"
		    return message, 400
		# We allow the length of the new value to be 0
		student[key] = value
        batch_update(students)
    except:
        return "You must initiate the value of the field to something - it cannot be blank\n", 400
    return "Schema successfully updated"

# DELETE .../K12/schema/table/<key> - Delete a column from the table schema
@app.route('/K12/schema/table/<key>', methods = ['DELETE'])
def delete_schema(key):
    try:
        regex = re.compile('[^0-9a-zA-Z]')
        key = regex.sub('', key)
	print "Regexed: " + key
    except:
        return "Bad request, improper key format", 400
    if len(key) < 1:
	return "Bad request, improper key format", 400
    if key == 'uid':
        return "Deleting a student's uid is forbidden\n", 422
    students = find_all_items()
    for student in students:
        uid = student['uid']
        try:
            del student[key]
        except KeyError:
            pass
    batch_update(students)
    return "Schema key(" + key + ") successfully deleted", 200

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

#==============================================================================
# Helper Methods
#==============================================================================

# Returns data whether from request.form or request.data
def form_or_json():
    data = request.data
    return json.loads(data) if data is not '' else request.form

if __name__ == '__main__':
    app.run(
        debug = True,
        port = 9002
    )
