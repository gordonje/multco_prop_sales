from datetime import datetime
from http_helpers import login, get_property, get_search_results
from db_helpers import get_conn_string, query, query_w_results, insert_data
from parsers import make_soup, parse_address, parse_property
import requests


start_time = datetime.now()
print 'Started at {}'.format(start_time)

conn_string = get_conn_string()


# get all distinct properties to request, excluding those we already have
property_ids = [] 


for i in query_w_results(conn_string, '''SELECT DISTINCT property_id 
										FROM cash_sales_orig 
										WHERE property_id NOT IN (SELECT property_id FROM properties);'''):
	property_ids.append(i['property_id'])


with requests.session() as session:

	login(session)

	for prop_id in property_ids:

		if (datetime.now().hour - start_time.hour) > 11:
			print '   Time to login...'
			login(session)

		run_time = datetime.now() - start_time

		print 'Requesting prop_id {0} (runtime = {1})...'.format(prop_id, run_time)

		soup = make_soup(get_property(session, prop_id))

		prop = parse_property(soup, prop_id)

		if prop != None:
			
			insert_data(conn_string, prop)

print 'fin'
