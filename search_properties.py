from datetime import datetime
from http_helpers import login, get_property, get_search_results
from db_helpers import get_conn_string, query, query_w_results
from parsers import make_soup, has_next_button, parse_results_page, match_site_address
from parsers import parse_address, parse_property
import requests


start_time = datetime.now()
print 'Started at ' + str(start_time)

conn_string = get_conn_string()

query(conn_string, open("sql/create_searches.sql", "r").read())
query(conn_string, open("sql/create_properties.sql", "r").read())
query(conn_string, open("sql/create_property_sales.sql", "r").read())


# get all a address from cash sales that don't currently have a property_id
addresses = query_w_results(conn_string, '''SELECT DISTINCT 
												  zip
												, street_no
												, street_dir
												, street
												, street_typ
												, unit_no 
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
			, 'possible_matches_num': 0
			, 'possible_matches': []
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

						data['possible_matches'].append(possible_match)

				page_num += 1

			else:

				print 'No results.'

		data['possible_matches_num'] = len(data['possible_matches'])

		query(conn_string, '''INSERT INTO searches (
									  search_id
									, street_no
									, street_dir
									, street
									, street_typ
									, unit_no
									, zip
									, results_num
									, possible_matches_num
								) VALUES (
									  %(search_id)s
									, %(street_no)s
									, %(street_dir)s
									, %(street)s
									, %(street_typ)s
									, %(unit_no)s
									, %(zip)s
									, %(results_num)s
									, %(possible_matches_num)s
								);''',
			data)

		for property_id in data['possible_matches']:

			soup = make_soup(get_property(session, property_id))

			prop = parse_property(soup, property_id, data['search_id'])

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
				(property_id, search_id) + sale)

		search_id += 1

		print '============'

