from sys import argv
from getpass import getpass
import psycopg2

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
		with conn.cursor() as cur:
			cur.execute(operation, parameters)
			return cur.fetchall()