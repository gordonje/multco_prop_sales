CREATE TABLE IF NOT EXISTS properties (
          id varchar(8) PRIMARY KEY
        , owner_names varchar(255)
        , owner_address_line1 varchar(255)
        , owner_address_line2 varchar(255)
        , owner_address_line3 varchar(255)
        , situs_address_line1 varchar(255)
        , situs_address_line2 varchar(255)
        , situs_address_line3 varchar(255)
        , html text
);

CREATE TABLE IF NOT EXISTS property_sales (
          property_id varchar(8) REFERENCES properties(id)
        , deed varchar(8)
        , seller varchar(255)
        , buyer varchar(255)
        , instrument varchar(255)
        , date_sale date
        , consideration_amount int
);