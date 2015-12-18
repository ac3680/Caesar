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
### Test Cases
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

5. 
