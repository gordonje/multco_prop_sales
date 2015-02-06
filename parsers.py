from bs4 import BeautifulSoup, NavigableString
import re
from datetime import datetime


def make_soup(response):
	return BeautifulSoup(response.content)


def has_next_button(response_soup):
	# Takes soup, searches for the Next button and returns True if found

	if response_soup.find('input', {'type': 'button', 'value': 'Next'}) != None:
		return True
	else: 
		return False


def parse_results_page(response_soup):
	# Takes soup, searches for the tags containing the property_id, returns a list of the tags

	prop_tags = []

	results = response_soup.find_all('td', class_ = 'prop')

	for prop in results:

		property_id = prop.find('a').text.strip()
		
		if len(property_id) > 0:

			prop_tags.append(prop)

	return prop_tags


def match_site_address(prop_tag, address_dict):
	# Takes a property tag and an address dictionary, sees if the address info of the property matches 
	# the address in the dictionary. If so, returns the property_id

	for key in address_dict:
		if address_dict[key] == None:
			address_dict[key] = ''

	zipcode =  prop_tag.find_next_siblings('td')[2].contents[2].split(', OR ')[1].strip()
	result_address = prop_tag.find_next_siblings('td')[2].contents[0].strip()

	print 'Result address: ' + result_address

	if int(zipcode) == address_dict['zip']:
		if re.match('\d{{0,}}{street_no} {street_dir} {street} {street_typ}[^1-9]{{0,}}{unit_no}'.format(**address_dict).strip(), result_address, flags=re.IGNORECASE):
			return prop_tag.text.strip()


def parse_address(address_tag):
	# takes a bs4.tag containing address info and returns a list containing three address lines.
	
	address_list = []

	for i in address_tag.descendants:
		if isinstance(i, NavigableString):
			address_list.append(i.strip())
	# make sure that there are three items in the address list. Pass None (saves to db as null) for empty address lines.
	for i in range(len(address_list), 3):
		address_list.append(None)

	return address_list



def parse_property(response_soup, property_id, search_id):
	# Takes soup and parses out all of the property info.

	try:
		owner_names = response_soup.find_all('tr', class_ = 'regtxt')[0].find('td').text.strip()
	except Indexerror:
		print response_soup

	owner_address = parse_address(response_soup.find_all('tr', class_ = 'regtxt')[1].find_all('td')[0])

	situs_address = parse_address(response_soup.find_all('tr', class_ = 'regtxt')[1].find_all('td')[1])

	prop = {
		  'property_id': property_id
		, 'search_id': search_id
		, 'owner_names': owner_names
		, 'owner_address_line1': owner_address[0]
		, 'owner_address_line2': owner_address[1]
		, 'owner_address_line3': owner_address[2]
		, 'situs_address_line1': situs_address[0]
		, 'situs_address_line2': situs_address[1]
		, 'situs_address_line3': situs_address[2]
		, 'html': response_soup.prettify()
		, 'sales_records': []
	}

	for tr in response_soup.find('table', id = 'Table1').find_all('tr', class_ = 'regtxt'):

		sales_record = []

		counter = 0

		for td in tr.find_all('td'):

			if td.text.strip() == '':
				sales_record.append(None)
			else:
				if counter == 4:
					sales_record.append(datetime.strptime(td.text.strip(), "%m/%d/%y"))
				elif counter == 5:
					sales_record.append(int(td.text.replace('$', '').replace(',', '').strip()))		
				else:
					sales_record.append(td.text.strip())

			counter += 1

		prop['sales_records'].append(tuple(sales_record))

	return prop

