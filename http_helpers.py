from time import sleep


def login(request_session):
	# makes a post request with correct form data to default.asp
	payload = {
	  'buttonChoice': 2
	, 'UserId': 'guest'
	, 'ValidationReq': 1
	, 'ValidationReqGuest': 2
	}

	print '   Logging in...'

	try:
		response = request_session.post('http://multcoproptax.org/default.asp', data=payload)
	except:
		print '   Failed to log in.'

	return


def request_property(request_session, property_id):
	# waits 3 seconds, then makes a get request and returns response. 
	# if there's a connection error, reset the session and re-log in before trying again.
	sleep(3)

	payload = {'PropertyID': property_id}

	try:
		response = request_session.get('http://multcoproptax.org/property.asp', params = payload)
	except requests.exceptions.ConnectionError:
		# figure out how to print the specific kind of error
		print requests.exceptions.ConnectionError
		print '   Connection dropped, resetting session...'
		request_session = requests.Session()
		login(request_session)
		return make_request(request_session, payload)
	
	return response


# def request_search(request_session, address_dict):
# 	# waits 3 seconds, then makes a get request and returns response. 
# 	# if there's a connection error, reset the session and re-log in before trying again.
# 	sleep(3)

# 	try:
# 		response = request_session.post('http://multcoproptax.org/search.asp', address_dict)
# 	except requests.exceptions.ConnectionError:
# 		# figure out how to print the specific kind of error
# 		print requests.exceptions.ConnectionError
# 		print '   Connection dropped, resetting session...'
# 		request_session = requests.Session()
# 		login(request_session)
# 		return request_property(request_session, payload)
	
# 	return response