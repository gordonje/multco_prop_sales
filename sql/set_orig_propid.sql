UPDATE cash_sales_orig
SET property_id = appd.propertyid
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
  AND appd.propertyid IS NOT NULL;