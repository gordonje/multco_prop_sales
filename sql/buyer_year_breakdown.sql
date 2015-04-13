SELECT
	  total.buyer AS total_buyer
	, total.buys AS total_buys
	, total.spent AS total_spent
	, Y2005.buys AS Y2005_buys 
	, Y2005.spent AS Y2005_spent 
	, Y2006.buys AS Y2006_buys 
	, Y2006.spent AS Y2006_spent 
	, Y2007.buys AS Y2007_buys 
	, Y2007.spent AS Y2007_spent 
	, Y2008.buys AS Y2008_buys 
	, Y2008.spent AS Y2008_spent 
	, Y2009.buys AS Y2009_buys 
	, Y2009.spent AS Y2009_spent 
	, Y2010.buys AS Y2010_buys 
	, Y2010.spent AS Y2010_spent 
	, Y2011.buys AS Y2011_buys 
	, Y2011.spent AS Y2011_spent 
	, Y2012.buys AS Y2012_buys 
	, Y2012.spent AS Y2012_spent 
	, Y2013.buys AS Y2013_buys 
	, Y2013.spent AS Y2013_spent 
	, Y2014.buys AS Y2014_buys 
	, Y2014.spent AS Y2014_spent 
FROM (
	SELECT 
		  buyer
		, COUNT(*) AS buys
		, SUM(consideration_amount) AS spent
	FROM cash_sales_matches
	GROUP BY 1
) AS total
LEFT JOIN (
	SELECT 
		  buyer
		, COUNT(*) AS buys
		, SUM(consideration_amount) spent
	FROM cash_sales_matches
	WHERE EXTRACT(year from date_sale)::INT = 2005
	GROUP BY 1
) AS Y2005
ON Y2005.buyer = total.buyer
LEFT JOIN (
	SELECT 
		  buyer
		, COUNT(*) AS buys
		, SUM(consideration_amount) spent
	FROM cash_sales_matches
	WHERE EXTRACT(year from date_sale)::INT = 2006
	GROUP BY 1
) AS Y2006
ON Y2006.buyer = total.buyer
LEFT JOIN (
	SELECT 
		  buyer
		, COUNT(*) AS buys
		, SUM(consideration_amount) spent
	FROM cash_sales_matches
	WHERE EXTRACT(year from date_sale)::INT = 2007
	GROUP BY 1
) AS Y2007
ON Y2007.buyer = total.buyer
LEFT JOIN (
	SELECT 
		  buyer
		, COUNT(*) AS buys
		, SUM(consideration_amount) spent
	FROM cash_sales_matches
	WHERE EXTRACT(year from date_sale)::INT = 2008
	GROUP BY 1
) AS Y2008
ON Y2008.buyer = total.buyer
LEFT JOIN (
	SELECT 
		  buyer
		, COUNT(*) AS buys
		, SUM(consideration_amount) spent
	FROM cash_sales_matches
	WHERE EXTRACT(year from date_sale)::INT = 2009
	GROUP BY 1
) AS Y2009
ON Y2009.buyer = total.buyer
LEFT JOIN (
	SELECT 
		  buyer
		, COUNT(*) AS buys
		, SUM(consideration_amount) spent
	FROM cash_sales_matches
	WHERE EXTRACT(year from date_sale)::INT = 2010
	GROUP BY 1
) AS Y2010
ON Y2010.buyer = total.buyer


LEFT JOIN (
	SELECT 
		  buyer
		, COUNT(*) AS buys
		, SUM(consideration_amount) spent
	FROM cash_sales_matches
	WHERE EXTRACT(year from date_sale)::INT = 2011
	GROUP BY 1
) AS Y2011
ON Y2011.buyer = total.buyer
LEFT JOIN (
	SELECT 
		  buyer
		, COUNT(*) AS buys
		, SUM(consideration_amount) spent
	FROM cash_sales_matches
	WHERE EXTRACT(year from date_sale)::INT = 2012
	GROUP BY 1
) AS Y2012
ON Y2012.buyer = total.buyer
LEFT JOIN (
	SELECT 
		  buyer
		, COUNT(*) AS buys
		, SUM(consideration_amount) spent
	FROM cash_sales_matches
	WHERE EXTRACT(year from date_sale)::INT = 2013
	GROUP BY 1
) AS Y2013
ON Y2013.buyer = total.buyer
LEFT JOIN (
	SELECT 
		  buyer
		, COUNT(*) AS buys
		, SUM(consideration_amount) spent
	FROM cash_sales_matches
	WHERE EXTRACT(year from date_sale)::INT = 2014
	GROUP BY 1
) AS Y2014
ON Y2014.buyer = total.buyer
ORDER BY total.buys DESC;