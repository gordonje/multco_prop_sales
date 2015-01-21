-- create a table of cash buyers
CREATE TABLE cash_buyers AS
SELECT 
          buyer
        , COUNT(*) AS num_cash_buys
        , SUM(consideration_amount) AS total_cash_spent
FROM cash_sales_matches
GROUP BY buyer
ORDER BY COUNT(*) DESC;

-- create a table of cash sellers
CREATE TABLE cash_sellers AS
SELECT 
          seller
        , COUNT(*) AS num_cash_sales
        , SUM(consideration_amount) AS total_cash_income
FROM cash_sales_matches
GROUP BY seller
ORDER BY COUNT(*) DESC;

-- create bought for / sold for table
CREATE TABLE cash_buys_sales AS
SELECT 
          a.property_id
        , a.buyer as cash_buyer
        , b.buyer as sold_to
        , a.consideration_amount as bought_for
        , b.consideration_amount as sold_for
        , b.consideration_amount - a.consideration_amount as net
FROM cash_sales_matches a
JOIN property_sales b
ON a.property_id = b.property_id
AND a.buyer = b.seller;
