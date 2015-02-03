CREATE TABLE IF NOT EXISTS searches (
	  search_id INT PRIMARY KEY
	, street_no INT
	, street_dir VARCHAR(2)
	, street VARCHAR(50)
	, street_typ VARCHAR(12)
	, unit_no VARCHAR(15)
	, zip INT
	, results_num INT
	, possible_matches_num INT
);