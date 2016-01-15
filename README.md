multo_prop_taxes
================

This is a repo for a project on which I collaborated with another investigative journalist in Oregon. We started of as scraping Multnomah County, Oregon, property sales information from [http://multcoproptax.org/](http://multcoproptax.org/), then sort of snowballed from there.


Dependencies
------------

*	[Python 2.7](https://www.python.org/ "Python 2.7") a scripting language
*	[requests](http://docs.python-requests.org/en/latest/ "Requests") for HTTP requests and responses
*	[beautifulsoup 4](http://www.crummy.com/software/BeautifulSoup/ "BeautifulSoup4") for parsing HTML
*	[PostgreSQL 9.3 +](http://www.postgresql.org/ "PostgreSQL") for storing and querying data
*	[psycopg2](http://initd.org/psycopg/ "psycopg2") for connecting Python to the database


Set up
------

First, you need to set up a local PostgreSQL database:

	$ psql
	# CREATE DATABASE [db_name];
	# \q

Now navigate into the project directory and run [setup_db.py](https://github.com/gordonje/multco_prop_sales/blob/master/setup_db.py):

	$ python setup_db.py [db_name] [db_user] [db_password]

If you don't pass the database connection parameters when you initiate the script, you'll be prompted to provide them.

This script creates tables for our original datasets--the [cash sales](https://github.com/gordonje/multco_prop_sales/blob/master/input/2014-12-12_Lee_van_der_Voo-Cash_Sales_Multnomah.csv) and the [cash sales with some property data appended](https://github.com/gordonje/multco_prop_sales/blob/master/input/MultcoCashRealEstateTransactions.csv)--then imports this data, adds serialized id field to each table and applies some indexes to each table.

Next, we add a property id column to cash_sales_orig and [populate it](https://github.com/gordonje/multco_prop_sales/blob/master/sql/set_orig_propid.sql) by joining to cash_sales_appd using the distinct address field values. This is the table of records we'll used to make our requests.

Finally, we create a couple other tables to hold the data to be scraped: the [properties](https://github.com/gordonje/multco_prop_sales/blob/master/sql/create_properties.sql) table and the [property_sales](https://github.com/gordonje/multco_prop_sales/blob/master/sql/create_property_sales.sql) table.


Requesting by property_id
-------------------------

For many addresses, we already have the property_id, so we can request these properties directly without having to search for them.

	$ python get_properties.py [db_name] [db_user] [db_password]

After connecting to the database, it selects into memory all the distinct property ids that have not yet been scraped. Then it sets up a request session, logs into multcoproptax.org and, for each property_id, makes a GET request to the [property.asp](http://multcoproptax.org/property.asp?PropertyID=R238620) page. If the request fails due to a connection error (e.g., if the server doesn't respond), then it resets the session, logs in again, and re-submits the request.

Once a valid response is received, we parse out and store the desired info for the property. Specifically, we grab:
*	Owner Names
*	Owner Address, which is parsed into three separate address lines
*	Situs Address, which is also parsed into three address lines
*	Each row in the Sales Information table:
	- Deed
	- Grantor (Seller)
	- Grantee (Buyer)
	- Instrument
	- Sales date
	- Consideration Amount

Note that the script is set to pause for three seconds before making a request so that we don't overwhelm the server. After accounting for the time spent waiting for a response, parsing the response and saving to the database, each property_id iteration take about six seconds. So if you're requesting several thousand property_ids, then script will need lots of uninterrupted time. For example, we had over 10,000 property_ids in the original use case, which required 16 to 17 hours total.


Searching for properties
------------------------

In some cases, we don't have a property_id, though we do have address information (i.e., street number, street direction, street name, street type, unit number and zip code) which may help us identify that specific property.


Matching cash sales
-------------------

	$ python matcher.py [db_name] [db_user] [db_password]


Outputs
-------

	$ python outputs.py [db_name] [db_user] [db_password]