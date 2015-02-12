from db_helpers import get_conn_string, query, query_w_results
from os import getcwd

conn_string = get_conn_string()


print 'Importing original cash sales...'

query(conn_string, open("sql/create_cash_sales_orig.sql", "r").read())

query(conn_string, '''COPY cash_sales_orig 
						FROM %s
						WITH CSV HEADER NULL 'NULL';'''
					, (getcwd() + '/input/2014-12-12_Lee_van_der_Voo-Cash_Sales_Multnomah.csv',)
				)

query(conn_string, 'ALTER TABLE cash_sales_orig ADD COLUMN id SERIAL PRIMARY KEY;')

query(conn_string, open("sql/index_cash_sales_orig.sql", "r").read())


print 'Importing appended cash sales...'

query(conn_string, open("sql/create_cash_sales_appd.sql", "r").read())

query(conn_string, '''COPY cash_sales_appd 
						FROM %s
						WITH CSV HEADER NULL '';'''
					, (getcwd() + '/input/MultcoCashRealEstateTransactions.csv',)
				)

query(conn_string, 'ALTER TABLE cash_sales_appd ADD COLUMN id SERIAL PRIMARY KEY;')

query(conn_string, open("sql/index_cash_sales_appd.sql", "r").read())


print 'Populating property_IDs on original cash sales...'

query(conn_string, 'ALTER TABLE cash_sales_orig ADD COLUMN property_id VARCHAR(7);')

query(conn_string, open("sql/set_orig_propid.sql", "r").read())

query(conn_string, 'CREATE INDEX ON cash_sales_orig(property_id);')


print 'Creating properties table...'

query(conn_string, open("sql/create_properties.sql", "r").read())


print 'Creating property_sales table...'

query(conn_string, open("sql/create_property_sales.sql", "r").read())

print 'fin.'