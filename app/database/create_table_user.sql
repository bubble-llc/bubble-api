CREATE TABLE IF NOT EXISTS user_table(
	username VARCHAR(256) PRIMARY KEY,
	password VARCHAR(256) NOT NULL,
	email VARCHAR(256) NOT NULL,
	date_joined timestamptz
);