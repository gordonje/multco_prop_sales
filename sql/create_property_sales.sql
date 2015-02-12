CREATE TABLE IF NOT EXISTS property_sales (
          sale_id SERIAL PRIMARY KEY
        , property_id varchar(8) REFERENCES properties(property_id)
        , search_id INT
        , deed varchar(8)
        , seller varchar(255)
        , buyer varchar(255)
        , instrument varchar(255)
        , date_sale date
        , consideration_amount int
);