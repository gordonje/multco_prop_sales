-- create and appended properties table
CREATE TABLE properties_appd AS
SELECT 
          properties.property_id
        , street_no
        , street_dir
        , street
        , street_typ
        , unit_no
        , zip
        , situs_address_line1 as address
        , sitecity as city
        , site_state as state
        , state_id
        , rno
        , owner_names
        , owner1
        , owner2
        , owner3
        , owneraddr
        , ownercity
        , ownerstate
        , ownerzip
        , legal_desc
        , taxcode
        , prop_code
        , prpcd_desc
        , landuse
        , yearbuilt
        , bldgsqft
        , bedrooms
        , floors
        , units
        , mktvalyr1
        , landval1
        , bldgval1
        , totalval1
        , mktvalyr2
        , landval2
        , bldgval2
        , totalval2
        , mktvalyr3
        , landval3
        , bldgval3
        , totalval3
        , acc_status
        , a_t_sqft
        , a_t_acres
        , frontage
        , county
        , source
        , tlid
FROM properties
LEFT JOIN cash_sales_appd
ON properties.property_id = cash_sales_appd.propertyid;

