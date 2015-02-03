CREATE TABLE IF NOT EXISTS properties (
          property_id VARCHAR(8) PRIMARY KEY
        , search_id INT REFERENCES searches(search_id)
        , owner_names VARCHAR(255)
        , owner_address_line1 VARCHAR(255)
        , owner_address_line2 VARCHAR(255)
        , owner_address_line3 VARCHAR(255)
        , situs_address_line1 VARCHAR(255)
        , situs_address_line2 VARCHAR(255)
        , situs_address_line3 VARCHAR(255)
        , html text
);