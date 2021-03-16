CREATE TABLE IF NOT EXISTS category_table(
	category_name VARCHAR(256) PRIMARY KEY,
	owner_username VARCHAR(256) REFERENCES user_table,
	date_created timestamptz
);
