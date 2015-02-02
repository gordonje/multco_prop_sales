CREATE INDEX ON cash_sales_appd (propertyid);

CREATE INDEX ON cash_sales_appd (zip);

CREATE INDEX ON cash_sales_appd (STREET_NO);

CREATE INDEX ON cash_sales_appd ((upper(STREET_DIR)));

CREATE INDEX ON cash_sales_appd ((upper(STREET)));

CREATE INDEX ON cash_sales_appd ((upper(STREET_TYP)));

CREATE INDEX ON cash_sales_appd ((upper(unit_no)));

CREATE INDEX ON cash_sales_appd (SALEDATE);

CREATE INDEX ON cash_sales_appd (SALEPRICE);

