multo_prop_taxes
================

For scraping Multnomah County, Oregon, property tax information from [http://multcoproptax.org/](http://multcoproptax.org/).


Dependencies
------------

*	[Python 2.7](https://www.python.org/ "Python 2.7") a scripting language
*	[requests](http://docs.python-requests.org/en/latest/ "Requests") for HTTP requests and responses
*	[beautifulsoup 4](http://www.crummy.com/software/BeautifulSoup/ "BeautifulSoup4") for parsing HTML
*	[PostgreSQL 9.3 +](http://www.postgresql.org/ "PostgreSQL") for storing querying data
*	[psycopg2](http://initd.org/psycopg/ "psycopg2") for connecting to the database


How it works (in a nutshell)
----------------------------

In the terminal, type:

	python get_property_taxes.py [name of database] [db user name] [db user password]

If you don't pass the database connection parameters when you initiate the script, you will be prompted to provide them.

Unless they already exist in your database, the script will [create the necessary tables](https://github.com/gordonje/multco_prop_taxes/blob/master/create_tables.sql).

It reads in a list of property IDs from the [PIDs.txt](https://github.com/gordonje/multco_prop_taxes/blob/master/PIDs.txt) file, excluding any duplicates in the file. It also selects all of the property_ids currently in the database. As the script iterates over the desired property_ids, it checks to see if the database already has a record for that property_id, in which case it doesn't request more info about it. (Though, it occurs to me that, were this an on-going data-mining project, it would be probably be necessary to make the requests anyway in order to update information, like the current owners and add new sales records).

In order to submit requests, the script first sets up a request session and logs into [http://multcoproptax.org](http://multcoproptax.org). Then for each property_id (after checking whether or not it needs to make a request for it), it makes a GET request to the [property.asp](http://multcoproptax.org/property.asp?PropertyID=R238620) page. If the request fails due to a connection error (e.g., if the server doesn't respond), then it resets the session, logs in again, and re-submits the request.

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
