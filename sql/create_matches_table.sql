CREATE TABLE IF NOT EXISTS cash_sales_matches (
          cash_sales_id BIGINT REFERENCES cash_sales_orig(id)
        , prop_sales_id BIGINT REFERENCES property_sales(sales_id)
        , property_id VARCHAR(8) REFERENCES properties(property_id)
        , date_coe DATE
        , date_sale DATE
        , date_diff SMALLINT
        , consideration_amount INT
        , deed VARCHAR(8)
        , seller VARCHAR(255)
        , buyer VARCHAR(255)
        , instrument VARCHAR(255)
        , street_no INT
        , street_dir VARCHAR(2)
        , street VARCHAR(50)
        , street_typ VARCHAR(5)
        , unit_no VARCHAR(10)
        , zip INT
        , PRIMARY KEY (cash_sales_id, prop_sales_id)
);