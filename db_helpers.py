from sys import argv
from getpass import getpass
import psycopg2
import psycopg2.extras


def get_conn_string():
	# returns a valid connection string to use when getting to db via psycopg2

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

	return "dbname=%(db)s user=%(user)s password=%(password)s" % {"db": db, "user": user, "password": password}


def query(conn_string, operation, parameters = None):

	with psycopg2.connect(conn_string) as conn:
		with conn.cursor() as cur:
			cur.execute(operation, parameters)


def query_w_results(conn_string, operation, parameters = None):

	with psycopg2.connect(conn_string) as conn:
		with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
			cur.execute(operation, parameters)
			return cur.fetchall()

def insert_data(conn_string, prop):

	is_dupe = False;

	try:
		query(conn_string, '''INSERT INTO properties (
								  property_id
								, search_id
								, owner_names
								, owner_address_line1
								, owner_address_line2
								, owner_address_line3
								, situs_address_line1
								, situs_address_line2
								, situs_address_line3
								, html
							) VALUES (
								  %(property_id)s
								, %(search_id)s
								, %(owner_names)s
								, %(owner_address_line1)s
								, %(owner_address_line2)s
								, %(owner_address_line3)s
								, %(situs_address_line1)s
								, %(situs_address_line2)s
								, %(situs_address_line3)s
								, %(html)s
							);''', 
		prop)
	except psycopg2.IntegrityError:
		print '   Duplicate property_id.'
		is_dupe	= True

	if is_dupe:
		pass
	else:
		for sale in prop['sales_records']:

			query(conn_string, '''INSERT INTO property_sales (
									  property_id
									, search_id
									, deed
									, seller
									, buyer
									, instrument
									, date_sale
									, consideration_amount
								) VALUES (
									  %s
									, %s
									, %s
									, %s
									, %s
									, %s
									, %s
									, %s
							);''', 
			(prop['property_id'], prop['search_id']) + sale)
