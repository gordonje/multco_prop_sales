-- there are no appended cash sales records with the multiple propertyIDs for the same
-- zip, street_no, street, street_dir, street_typ and unit_no combos
SELECT
          zip
        , street_no
        , street
        , street_dir
        , street_typ
        , unit_no
        , count(*) as the_count
FROM (
        SELECT
                  zip
                , street_no
                , street
                , street_dir
                , street_typ
                , unit_no
                , propertyid
                , count(*) as the_count
        FROM cash_sales_appd
        GROUP BY 1, 2, 3, 4, 5, 6, 7
) as appd
WHERE propertyid is not NULL
GROUP BY 1, 2, 3, 4, 5, 6
HAVING COUNT(*) > 1;

-- which means we can safely add propertyID column to the cash_sales_orig table
ALTER TABLE cash_sales_orig ADD COLUMN propertyid VARCHAR(7);

-- and update it with the propertyids from the appd table
UPDATE cash_sales_orig
SET propertyid = appd.propertyid
FROM (
        SELECT
                  zip
                , street_no
                , street
                , street_dir
                , street_typ
                , unit_no
                , propertyid
        FROM cash_sales_appd
        GROUP BY 1, 2, 3, 4, 5, 6, 7
) as appd
WHERE cash_sales_orig.zip = appd.zip
  AND COALESCE(cash_sales_orig.street_no, 0) = COALESCE(appd.street_no, 0)
  AND COALESCE(cash_sales_orig.street, 'NULL') = COALESCE(appd.street, 'NULL')
  AND COALESCE(cash_sales_orig.street_dir, 'NULL') = COALESCE(appd.street_dir, 'NULL')
  AND COALESCE(cash_sales_orig.street_typ, 'NULL') = COALESCE(appd.street_typ, 'NULL')
  AND COALESCE(cash_sales_orig.unit_no, 'NULL') = COALESCE(appd.unit_no, 'NULL')
  AND appd.propertyid is not NULL;