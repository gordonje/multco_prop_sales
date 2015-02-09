INSERT INTO cash_sales_matches (
	  cash_sales_id
	, prop_sales_id
	, property_id
	, date_coe
	, date_sale
	, date_diff
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
)
SELECT 
	  a.id as cash_sale_id
	, b.sales_id as prop_sale_id
	, b.property_id
	, a.date_coe
	, b.date_sale
	, DATE_PART('day', AGE(date_coe, date_sale))::int as day_diff
	, b.consideration_amount
	, b.deed
	, b.seller
	, b.buyer
	, b.instrument
	, a.street_no
	, a.street_dir
	, a.street
	, a.street_typ
	, a.unit_no
	, a.zip
FROM cash_sales_orig a
JOIN property_sales b
ON a.property_id = b.property_id
AND a.date_coe = b.date_sale - %s
WHERE consideration_amount > 0
AND prop_type = 'Resid'
AND a.id not in (SELECT cash_sales_id FROM cash_sales_matches)
AND b.sales_id not in (SELECT prop_sales_id FROM cash_sales_matches);