from datetime import datetime
from http_helpers import login, get_property, get_search_results
from db_helpers import get_conn_string, query, query_w_results, insert_data
from parsers import make_soup, has_next_button, parse_results_page, match_site_address
from parsers import parse_address, parse_property
import requests


start_time = datetime.now()
print 'Started at ' + str(start_time)

conn_string = get_conn_string()

query(conn_string, open("sql/create_searches.sql", "r").read())

# get all a address from cash sales that don't currently have a property_id
addresses = query_w_results(conn_string, '''SELECT DISTINCT 
												  zip
												, street_no
												, street_dir
												, street
												, street_typ
												, replace(unit_no, '#', '') as unit_no 
											FROM cash_sales_orig
											WHERE property_id IS NULL;''')

# Determines which record with which to start searching
start_position = query_w_results(conn_string, '''SELECT COUNT(*) as the_count
												FROM searches;''')[0]['the_count']

search_id = start_position + 1

# for each address in the cash sales where we don't have a propertyid

with requests.session() as session:

	login(session)

	for i in addresses[start_position:]:

		if (datetime.now().hour - start_time.hour) > 11:
			print '   Time to login...'
			login(session)

		print "Search criteria: {street_no} {street_dir} {street} {street_typ} {unit_no} {zip}".format(**i)

		data = {
			  'search_id': search_id
			, 'street_no': i['street_no']
			, 'street_dir': i['street_dir']
			, 'street': i['street']
			, 'street_typ': i['street_typ']
			, 'unit_no': i['unit_no']
			, 'zip': i['zip']
			, 'results_num': 0
			, 'address_matches_num': 0
			, 'zip_matches_num': 0
			, 'address_matches': []
			, 'zip_matches': []
			, 'property_id': None
		}

		more_results = True
		page_num = 1

		while more_results:

			print '   Trying page #' + str(page_num)
		
			soup = make_soup(get_search_results(session, i, page_num))

			more_results = has_next_button(soup)

			props = parse_results_page(soup)

			if len(props) > 0:

				data['results_num'] += len(props)

				for prop in props:

					possible_match = match_site_address(prop, i)

					if possible_match != None:
						if possible_match['type'] == 'address_match':
							data['address_matches'].append(possible_match['property_id'])
						if possible_match['type'] == 'zip_match':
							data['zip_matches'].append(possible_match['property_id'])

				page_num += 1

			else:

				print 'No results.'

		data['address_matches_num'] = len(data['address_matches'])
		data['zip_matches_num'] = len(data['zip_matches'])

		if data['address_matches_num'] == 1:
			# if there's only one possible match, keep that property_id on the searches record for easier joining
			data['property_id'] = data['address_matches'][0]

		elif data['results_num'] == 1 and data['zip_matches'] == 1:
			# if there's only one result and one zip match, store this property_id
			data['property_id'] = data['zip_matches'][0]

		query(conn_string, '''INSERT INTO searches (
									  search_id
									, street_no
									, street_dir
									, street
									, street_typ
									, unit_no
									, zip
									, results_num
									, address_matches_num
									, zip_matches_num
									, property_id
								) VALUES (
									  %(search_id)s
									, %(street_no)s
									, %(street_dir)s
									, %(street)s
									, %(street_typ)s
									, %(unit_no)s
									, %(zip)s
									, %(results_num)s
									, %(address_matches_num)s
									, %(zip_matches_num)s
									, %(property_id)s
								);''',
			data)


		for property_id in data['address_matches']:

			soup = make_soup(get_property(session, property_id))

			prop = parse_property(soup, property_id, data['search_id'])

			insert_data(conn_string, prop)

		if data['results_num'] == 1 and data['address_matches'] == 0 and data['zip_matches'] == 1:

			soup = make_soup(get_property(session, data['property_id']))

			prop = parse_property(soup, property_id, data['search_id'])

			insert_data(conn_string, prop)

		search_id += 1

		print '============'

print 'fin.'

