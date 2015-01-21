-- create a table of cash buyers
CREATE TABLE cash_buyers AS
SELECT 
          buyer
        , COUNT(*) AS num_cash_buys
        , SUM(consideration_amount) AS cash_total
FROM cash_sales_matches
GROUP BY buyer
ORDER BY COUNT(*) DESC;

-- create a table of cash sellers
CREATE TABLE cash_sellers AS
SELECT 
          seller
        , COUNT(*) AS num_cash_sales
        , SUM(consideration_amount) AS cash_total
FROM cash_sales_matches
GROUP BY seller
ORDER BY COUNT(*) DESC;