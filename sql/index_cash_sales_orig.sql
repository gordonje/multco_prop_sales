CREATE INDEX ON cash_sales_orig (zip);

CREATE INDEX ON cash_sales_orig (date_coe);

CREATE INDEX ON cash_sales_orig (STREET_NO);

CREATE INDEX ON cash_sales_orig ((upper(STREET_DIR)));

CREATE INDEX ON cash_sales_orig ((upper(STREET)));

CREATE INDEX ON cash_sales_orig ((upper(STREET_TYP)));

CREATE INDEX ON cash_sales_orig ((upper(unit_no)));

CREATE INDEX ON cash_sales_orig ((upper(Prop_type)));