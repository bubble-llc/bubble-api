CREATE TABLE IF NOT EXISTS user_table(
	username VARCHAR(256) PRIMARY KEY,
	password VARCHAR(256) NOT NULL,
	email VARCHAR(256) NOT NULL UNIQUE,
	validation_code VARCHAR(256) NOT NULL,
	is_validated BOOLEAN DEFAULT false,
	date_joined timestamptz
);