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

