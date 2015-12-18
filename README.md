# Caesar

### Setup

Install the latest Boto 3 release via pip:

```pip install boto3```

Credentials for your AWS account can be found in the IAM Console. Create credentials file in ~/.aws/credentials:

```
[default]
aws_access_key_id = YOUR_ACCESS_KEY
aws_secret_access_key = YOUR_SECRET_KEY
```

Set a default region in ~/.aws/config:

```
[default]
region=us-east-1
```

Run `python createK12Table.py` to create your DynamoDB table.

Optionally run `python prepopulateK12Table.py` to populate your DynamoDB table with our group members.

Now you should be able to run `python K12InfoService.py`.

### Sample Curl Requests
```
# Regular requests
curl -X POST --data "uid=blanks&name=Nina Baculinao" http://localhost:9002/K12
curl -X GET http://localhost:9002/K12
curl http://localhost:9002/K12/blanks
curl -X PUT --data "school=SCE" http://localhost:9002/K12/blanks
curl -X DELETE http://localhost:9002/K12/blanks 

# Change schema
curl http://localhost:9002/K12
curl -X PUT --data "professor=Don" http://localhost:9002/K12/schema/table
curl http://localhost:9002/K12
curl -X DELETE http://localhost:9002/K12/schema/table/professor
curl http://localhost:9002/K12
```

```
### Test Cases
Testing POST
1. Nonsense uid
curl -X POST --data "uid=$@&name=Nina Baculinao" http://localhost:9002/K12
Expected response: Bad request, improper UID
Note: MS cannot survive certain bad inputs, such as additional &s in the data fields

2. Blank uid
curl -X POST --data "uid=&name=Nina Baculinao" http://localhost:9002/K12
Expected response: Bad request, improper UID

3. Nonsense student name
curl -X POST --data "uid=blanks&name=Nina$#@Baculinao" http://localhost:9002/K12

4. Existing student
curl -X POST --data "uid=blanks&name=Nina Baculinao Evil Twin/localhost:9002/K12
Expected response: The student(blanks) already exists

5. Empty name
curl -X POST --data "uid=bla--ncks&name=$" http://localhost:9002/K12
Expected response: Bad request, improper name

6. No name
api bluemelodia$ curl -X POST --data "uid=bla--ncks" http://localhost:9002/K12
Expected response: New student(blancks) created

7. No uid
curl -X POST --data "" http://localhost:9002/K12
Expected response: Need uid to create new student

8. Extra column
curl -X POST --data "uid=profwu&name=Eugene Wu&profession=Professor" http://localhost:9002/K12
Expected response: New student(profwu) created

Testing GET
1. curl -X GET http://localhost:9002/K12
Expected response: list of all the students
Can't really break this one

2. Nonexistent uid
curl -X GET http://localhost:9002/K12/peach
Expected response: {
  "message": "Not Found: http://localhost:9002/K12/peach", 
  "status": 404
}

3. Bad uid
curl -X GET http://localhost:9002/K12/$$$$$
Expected response: {
  "message": "Not Found: http://localhost:9002/K12/3597035970$", 
  "status": 404
}

4. Valid uid 
curl -X GET http://localhost:9002/K12/blanks
Expected response: {"name": "Nina Baculinao", "uid": "blanks"}

Testing PUT
1. Changing existing column 
curl -X PUT --data "school=SCE" http://localhost:9002/K12/blanks
Expected response: Student(blanks) updated successfully
curl -X GET http://localhost:9002/K12/blanks
{"school": "SCE", "name": "Nina Baculinao", "uid": "blanks"}

2. Changing non-existing column
curl -X PUT --data "iq=240" localhost:9002/K12/blanks
Expected response: Student(blanks) updated successfully
curl -X GET http://localhost:9002/K12/blanks
{"iq": "240", "school": "SCE", "name": "Nina Baculinao", "uid": "blanks"}

3. Changing column with blank value (intentionally)
curl -X PUT --data "iq=" localhost:9002/K12/blanks
Expected response: Bad request, improper iq

4. Changing column with blank value (through stripping of invalid characters)
curl -X PUT --data "iq=$" localhost:9002/K12/blanks
Expected response: Bad request, improper iq

5. Trying to change the uid
curl -X PUT --data "uid=$" localhost:9002/K12/blanks
Expected response: Updating a student's uid is forbidden

Testing DELETE
1. Existing uid
curl -X DELETE http://localhost:9002/K12/blanks 
Expected response: Student(blanks) deleted successfully
curl -X GET http://localhost:9002/K12/blanks
{
  "message": "Not Found: http://localhost:9002/K12/blanks", 
  "status": 404
}

2. Non-existing uid
curl -X DELETE http://localhost:9002/K12/blankss
Expected response: 
{
  "message": "Not Found: http://localhost:9002/K12/blankss", 
  "status": 404
}

3. Improper uid
curl -X DELETE http://localhost:9002/K12/#$#@!
Expected response: 
{
  "message": "Not Found: http://localhost:9002/K12/blankss", 
  "status": 404
}

Note: not all improper inputs will give this response, some will return 'Bad request, improper UID'

Testing Schema Change PUT
1. Add a new column
curl -X PUT --data "professor=Don" http://localhost:9002/K12/schema/table
Expected response: Schema successfully updated

2. Add an existing column 
curl -X PUT --data "school=Hogwarts" http://localhost:9002/K12/schema/table
Expected response: Schema successfully updated
[{"uid": "nb2406", "professor": "Don", "last_name": "B", "school": "Hogwarts", "first_name": "Nina"}, {"uid": "mlh2197", "professor": "Don", "last_name": "H", "school": "Hogwarts", "first_name": "Melanie"}, {"professor": "Don", "school": "Hogwarts", "uid": "drop", "name": "Nina Baculin"}, {"professor": "Don", "school": "Hogwarts", "uid": "bla--ncks"}, {"professor": "Don", "school": "Hogwarts", "uid": "blank", "name": "Nina Bac"}, {"professor": "Don", "school": "Hogwarts", "uid": "drop table", "name": "Nina Baculin"}, {"uid": "wvb2103", "professor": "Don", "last_name": "B", "school": "Hogwarts", "first_name": "Whitney"}, {"professor": "Don", "school": "Hogwarts", "uid": "drop table Students;", "name": "Nina Baculin"}, {"professor": "Don", "school": "Hogwarts", "uid": "bla", "name": "Nina0Baculinao"}, {"professor": "Don", "school": "Hogwarts", "uid": "K12InfoService.py#@K12InfoService.py", "name": "Nina Baculinao"}, {"professor": "Don", "school": "Hogwarts", "uid": "drop table --", "name": "Nina Baculin"}, {"professor": "Don", "school": "Hogwarts", "profession": "Professor", "uid": "profwu", "name": "EugeneWu"}, {"professor": "Don", "school": "Hogwarts", "uid": "blanks2", "name": "Nina0@Baculinao"}, {"professor": "Don", "school": "Hogwarts", "uid": "mmm", "name": "Nina Baculin"}, {"professor": "Don", "school": "Hogwarts", "uid": "blanks3", "name": "Nina0@Baculinao"}]Melanies-MBP:api bluemelodia$ 
Everyone goes to Hogwarts now

3. Try to add the uid column
curl -X PUT --data "uid=evil" http://localhost:9002/K12/schema/table
Expected response: Modifying a student's uid field is forbidden

4. Try to add a column with bad data 
curl -X PUT --data "professor=" http://localhost:9002/K12/schema/table
Expected response: You must initiate the value of the field to something - it cannot be blank

5. Update on a new schema field
GET http://localhost:9002/K12Eugene Wu" localhost:9002/K12/nb2406
Expected response: Student(nb2406) updated successfully
{"uid": "nb2406", "professor": "EugeneWu", "last_name": "B", "school": "Hogwarts", "first_name": "Nina"}

Testing Schema Change DELETE
1. Try to delete uid 
curl -X DELETE http://localhost:9002/K12/schema/table/uid
Expected response: Deleting a student's uid is forbidden

2. Try to delete something we never added 
curl -X DELETE http://localhost:9002/K12/schema/table/turtle
Expected response: Schema key(turtle) successfully deleted

3. Try to delete a valid field
curl -X DELETE http://localhost:9002/K12/schema/table/professor
Expected response: Schema key(professor) successfully deleted
Nobody has a professor now

Other


```
