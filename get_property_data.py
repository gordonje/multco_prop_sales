import requests
from time import sleep
from datetime import datetime
from sys import argv
from getpass import getpass
import psycopg2
from bs4 import BeautifulSoup, NavigableString


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


def make_request(request_session, request_data):
	# waits 3 seconds, then makes a get request and returns response. 
	# if there's a connection error, reset the session and re-log in before trying again.
	sleep(3)

	try:
		response = request_session.get('http://multcoproptax.org/property.asp', params = request_data)
	except requests.exceptions.ConnectionError:
		# figure out how to print the specific kind of error
		print requests.exceptions.ConnectionError
		print '   Connection dropped, resetting session...'
		request_session = requests.Session()
		login(request_session)
		return make_request(request_session, request_data)
	
	return response


def parse_address(address_tag):
	# takes a bs4.tag containing address info and returns a list containing three address lines.
	address_list = []

	for i in address_tag.descendants:
		if isinstance(i, NavigableString):
			address_list.append(i.strip())
	# make sure that there are three items in the address list. Pass None (saves to db as null) in for empty address lines.
	for i in range(len(address_list), 3):
		address_list.append(None)

	return address_list


start_time = datetime.now()
print 'Started at ' + str(start_time)


# read in the property_ids, excluding duplicates
property_ids = []

with open('PIDs.txt', 'rU') as f:
	for i in f:
		if i.strip() not in property_ids:
			property_ids.append(i.strip())


# Database connection setup
try:
	db = argv[1]
except IndexError:
	db = raw_input("Enter db name:")

try:
	user = argv[2]
except IndexError:
	user = raw_input("Enter db user:")

try:
	password = argv[3]
except IndexError:
	password = getpass("Enter db password:")

conn_string = "dbname=%(db)s user=%(user)s password=%(password)s" % {"db": db, "user": user, "password": password}


# create tables in database, unless they are already there
with psycopg2.connect(conn_string) as conn:
	with conn.cursor() as cur:
		cur.execute(open('create_tables.sql', "r").read())


# get all the property_ids currently saved in the database
prop_ids_in_db = []

with psycopg2.connect(conn_string) as conn:
	with conn.cursor() as cur:
		cur.execute('''SELECT id FROM properties;''')
		for i in cur.fetchall():
			prop_ids_in_db.append(i[0])



with requests.session() as session:

	login(session)

	for prop_id in property_ids:

		if prop_id not in prop_ids_in_db:

			runtime = datetime.now() - start_time

			print 'Requesting prop_id ' + prop_id + ' (runtime = ' + str(runtime) + ')...'

			payload = {'PropertyID': prop_id}

			prop = make_request(session, payload)

			soup = BeautifulSoup(prop.content)

			owner_names = soup.find_all('tr', class_ = 'regtxt')[0].find('td').text.strip()

			owner_address = parse_address(soup.find_all('tr', class_ = 'regtxt')[1].find_all('td')[0])

			situs_address = parse_address(soup.find_all('tr', class_ = 'regtxt')[1].find_all('td')[1])

			with psycopg2.connect(conn_string) as conn:
				with conn.cursor() as cur:
					cur.execute('''INSERT INTO properties (
										  id
										, owner_names
										, owner_address_line1
										, owner_address_line2
										, owner_address_line3
										, situs_address_line1
										, situs_address_line2
										, situs_address_line3										
										, html
									)
									VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);''', 
									(
										  prop_id
										, owner_names
										, owner_address[0]
										, owner_address[1]
										, owner_address[2]
										, situs_address[0]
										, situs_address[1]
										, situs_address[2]
										, soup.prettify()

									)
								)

			for tr in soup.find('table', id = 'Table1').find_all('tr', class_ = 'regtxt'):

				sales_record = [] 

				counter = 0

				for td in tr.find_all('td'):

					if td.text.strip() == '':
						sales_record.append(None)
					else:
						if counter == 4:
							sales_record.append(datetime.strptime(td.text.strip(), "%m/%d/%y"))
						elif counter == 5:
							sales_record.append(int(td.text.lstrip('$').strip().replace(',', '')))		
						else:
							sales_record.append(td.text.strip())

					counter += 1

				with psycopg2.connect(conn_string) as conn:
					with conn.cursor() as cur:
						cur.execute('''INSERT INTO property_sales (
									  property_id
									, deed
									, seller
									, buyer
									, instrument
									, date_sale
									, consideration_amount
								)
								VALUES (%s, %s, %s, %s, %s, %s, %s);''', 
								(
									  prop_id
									, sales_record[0]
									, sales_record[1]
									, sales_record[2]
									, sales_record[3]
									, sales_record[4]
									, sales_record[5]
								)
							)

print 'fin'
