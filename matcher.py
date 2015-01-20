import psycopg2

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

days_after = 0
days_before = 0

with psycopg2.connect(conn_string) as conn:
	with conn.cursor() as cur:
		cur.execute(open('sql/create_matches_table.sql', "r").read())	

with psycopg2.connect(conn_string) as conn:
	with conn.cursor() as cur:
		cur.execute(open('sql/exact_date_matches.sql', "r").read())	

while days_after < 7:
	days_after += 1
	with psycopg2.connect(conn_string) as conn:
		with conn.cursor() as cur:
			cur.execute(open('sql/days_after_matches.sql', "r").read(), (days_after, ))

while days_before < 4:
	days_before += 1
	with psycopg2.connect(conn_string) as conn:
		with conn.cursor() as cur:
			cur.execute(open('sql/days_before_matches.sql', "r").read(), (days_before, ))

while days_after < 30:
	days_after += 1
	with psycopg2.connect(conn_string) as conn:
		with conn.cursor() as cur:
			cur.execute(open('sql/days_after_matches.sql', "r").read(), (days_after, ))

	if days_after % 2 == 0:
		days_before += 1
		with psycopg2.connect(conn_string) as conn:
			with conn.cursor() as cur:
				cur.execute(open('sql/days_before_matches.sql', "r").read(), (days_before, ))