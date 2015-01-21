-- output properties appended table
COPY (
SELECT *
FROM properties_appd
) to '/Users/gordo/multco_prop_sales/output/properties_appd.csv' DELIMITER ',' CSV HEADER;

-- output cash matches table
COPY (
SELECT *
FROM cash_sales_matches
) to '/Users/gordo/multco_prop_sales/output/cash_sales_matches.csv' DELIMITER ',' CSV HEADER;

-- output unmatched cash sales
COPY (
SELECT *
FROM cash_sales_orig
WHERE id NOT IN (SELECT cash_sales_id FROM cash_sales_matches)
AND propertyid IS NOT NULL
) to '/Users/gordo/multco_prop_sales/output/cash_sales_unmatched.csv' DELIMITER ',' CSV HEADER;

-- output match duplicates
COPY (
SELECT *
FROM cash_sales_matches
WHERE cash_sales_id IN (
        SELECT cash_sales_id
        FROM cash_sales_matches
        GROUP BY cash_sales_id
        HAVING COUNT(*) > 1
)
ORDER BY property_id, date_sale DESC
) TO '/Users/gordo/multco_prop_sales/output/match_duplicates.csv' DELIMITER ',' CSV HEADER;

-- output flat file all sales
COPY (
SELECT 	  
	  b.id as prop_sales_id
	, a.property_id
	, date_sale
	, consideration_amount
	, deed
	, seller
	, buyer
	, instrument
	, street_no
        , street_dir
        , street
        , street_typ
        , unit_no
        , zip
        , address
        , city
        , state
        , state_id
        , rno
        , owner_names
        , owner1
        , owner2
        , owner3
        , owneraddr
        , ownercity
        , ownerstate
        , ownerzip
        , legal_desc
        , taxcode
        , prop_code
        , prpcd_desc
        , landuse
        , yearbuilt
        , bldgsqft
        , bedrooms
        , floors
        , units
        , mktvalyr1
        , landval1
        , bldgval1
        , totalval1
        , mktvalyr2
        , landval2
        , bldgval2
        , totalval2
        , mktvalyr3
        , landval3
        , bldgval3
        , totalval3
        , acc_status
        , a_t_sqft
        , a_t_acres
        , frontage
        , county
        , source
        , tlid
FROM properties_appd a
JOIN property_sales b
ON a.property_id = b.property_id
) to '/Users/gordo/multco_prop_sales/output/flat_file_all_sales.csv' DELIMITER ',' CSV HEADER;

-- output flat file cash only
COPY (
SELECT 	  
	  cash_sales_id
	, prop_sales_id
	, a.property_id
	, date_coe
	, date_sale
	, date_diff
	, consideration_amount
	, deed
	, seller
	, buyer
	, instrument
	, a.street_no
        , a.street_dir
        , a.street
        , a.street_typ
        , a.unit_no
        , a.zip
        , address
        , city
        , state
        , state_id
        , rno
        , owner_names
        , owner1
        , owner2
        , owner3
        , owneraddr
        , ownercity
        , ownerstate
        , ownerzip
        , legal_desc
        , taxcode
        , prop_code
        , prpcd_desc
        , landuse
        , yearbuilt
        , bldgsqft
        , bedrooms
        , floors
        , units
        , mktvalyr1
        , landval1
        , bldgval1
        , totalval1
        , mktvalyr2
        , landval2
        , bldgval2
        , totalval2
        , mktvalyr3
        , landval3
        , bldgval3
        , totalval3
        , acc_status
        , a_t_sqft
        , a_t_acres
        , frontage
        , county
        , source
        , tlid
FROM properties_appd a
JOIN cash_sales_matches b
ON a.property_id = b.property_id
) to '/Users/gordo/multco_prop_sales/output/flat_file_cash_only.csv' DELIMITER ',' CSV HEADER;

-- output cash buyers
COPY (
SELECT *
FROM cash_buyers
) TO '/Users/gordo/multco_prop_sales/output/cash_buyers.csv' DELIMITER ',' CSV HEADER;

-- output cash sellers
COPY (
SELECT *
FROM cash_sellers
) TO '/Users/gordo/multco_prop_sales/output/cash_sellers.csv' DELIMITER ',' CSV HEADER;

-- output cash_players
COPY (
SELECT 
          a.buyer as player
        , num_cash_buys
        , num_cash_sales
        , total_cash_spent
        , total_cash_income
        , total_cash_income - total_cash_spent as cash_net
FROM cash_buyers a
JOIN cash_sellers b
ON a.buyer = b.seller
ORDER BY total_cash_income - total_cash_spent DESC
) TO '/Users/gordo/multco_prop_sales/output/cash_players.csv' DELIMITER ',' CSV HEADER;

-- output all players
COPY (
SELECT 
          buyer
        , num_buys
        , num_sells
        , total_spent
        , total_income
        , total_income - total_spent AS total_net
FROM (
        SELECT buyer, COUNT(*) AS num_buys, SUM(consideration_amount) AS total_spent
        FROM property_sales
        GROUP BY buyer
) AS buyers
JOIN (
        SELECT seller, COUNT(*) AS num_sells, SUM(consideration_amount) AS total_income
        FROM property_sales
        GROUP BY seller
) AS sellers
ON buyers.buyer = sellers.seller
ORDER BY total_income - total_spent DESC
) TO '/Users/gordo/multco_prop_sales/output/all_players.csv' DELIMITER ',' CSV HEADER;

-- output cash_buys sold for
COPY (
SELECT *
FROM cash_buys_sales
ORDER BY net DESC
) TO '/Users/gordo/multco_prop_sales/output/cash_buys_sales.csv' DELIMITER ',' CSV HEADER;

-- output cash_buys_sales_sum
COPY (
SELECT 
          cash_buyer
        , COUNT(*) num_deals
        , SUM(net) as total_net
FROM cash_buys_sales
GROUP BY cash_buyer
ORDER BY SUM(net) DESC
) TO '/Users/gordo/multco_prop_sales/output/cash_buys_sales_sum.csv' DELIMITER ',' CSV HEADER;
