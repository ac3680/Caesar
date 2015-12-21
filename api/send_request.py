#Module to assist in calculating security signatures in order to make requests.

#To use as main, run python send_request.py "http request message"
#in command line.

#Example:
#python send_request.py "POST --data \"uid=blanks&name=Nina Baculinao\" http://localhost:9002/K12"

#Things to Note:
#1) You must put \ before every " in the command line
#2) You must enclose request in double quotes

import sys
import requests
import json
from SecurityService import encrypt

def send_request(request):

	#Look for the actual URL in input string.
	if "//" in request:
		index = request.find("//")
		index = index+2
		route = request[index:]
		index = route.find("/")
		route = route[index:]
		
	else:
		index = request.find("/")
		route = request[index:]

	
	#Op should be either get, post, delete, or put.
	req_list = request.split(" ")
	op = req_list[0]

	#Must have 'http://' in url to make request using requests
	#module.
	url = req_list[1]
	if url.find("http") < 0:
		url = "http://" + url
	
	get = "GET"
	post = "POST"
	put = "PUT"
	delete = "DELETE"

	hash_input = op.upper() + " " + str(route)


	#Make get requests.
	if(op.lower() == get.lower()):
		hash_value = encrypt(hash_input)

		signature = "\"signature\": \"" + str(hash_value) + "\""
		
		header = "{" + signature + "}"	
		header = json.loads(header)


		response = requests.get(url, headers=header)
		return response


	#Make delete requests.
	if(op.lower() == delete.lower()):
		hash_value = encrypt(hash_input)

		signature = "\"signature\": \"" + str(hash_value) + "\""
		header = "{" + signature + "}"	
		header = json.loads(header)

		response = requests.delete(url, headers=header)
		return response


	#Extract data from post and put requests.
	url_list = request.split("\"")
	data = url_list[1]
	data = "{\"" + data
	data = data.replace('=', '\":\"').replace('&', '\", \"')
	data = data + "\"}"
	data = json.loads(data)

	index = request.find("\"")
	
	after_quote = request[index:]
	after_quote = after_quote[1:]
		
	index = after_quote.find("\"")
	index = index+1
	
	#Recompute the URL based on something besides spaces.
	url = after_quote[index:]
	url = url.strip()

	#Must have 'http://' in url to make request using requests
	#module.
	if url.find("http") < 0:
		url = "http://" + url
	

	#Make post requests.
	if(op.lower() == post.lower()):
		hash_data = data
		
		for (key, value) in hash_data.iteritems():
			hash_input = hash_input + " " + str(value)

		hash_value = encrypt(hash_input)

		signature = "\"signature\": \"" + str(hash_value) + "\""
		
		header = "{" + signature + "}"	
		header = json.loads(header)

		response = requests.post(url, data=data, headers=header)
		return response


	#Make put requests.
	if(op.lower() == put.lower()):
		hash_data = data
		
		for (key, value) in hash_data.iteritems():
			hash_input = hash_input + " " + str(value)

		hash_value = encrypt(hash_input)
		
		signature = "\"signature\": \"" + str(hash_value) + "\""
		
		header = "{" + signature + "}"	
		header = json.loads(header)

		response = requests.put(url, data=data, headers=header)
		return response


	return "Error: Request is not get, post, put, or delete."
	

if __name__ == "__main__":
	arg = sys.argv[1:]
	request = arg[0]
	response = send_request(request)
	print response
	print response.text

