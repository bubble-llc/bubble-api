CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE IF NOT EXISTS user_table(
	username VARCHAR(256) PRIMARY KEY,
	password VARCHAR(256) NOT NULL,
	email VARCHAR(256) NOT NULL UNIQUE,
	validation_code VARCHAR(256) NOT NULL,
	is_validated BOOLEAN DEFAULT false,
	date_joined timestamptz
);

CREATE TABLE IF NOT EXISTS category_table(
	category_name VARCHAR(256) PRIMARY KEY,
	owner_username VARCHAR(256) REFERENCES user_table,
	date_created timestamptz
);

CREATE TABLE IF NOT EXISTS post_table(
	post_id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
	username VARCHAR(256) REFERENCES user_table,
	category_name VARCHAR(256) REFERENCES category_table,
	title varchar(256),
	content TEXT,
	latitude REAL,
	longitude REAL,
	date_created timestamptz,
	votes INTEGER DEFAULT 0,
	is_deleted BOOLEAN DEFAULT false,
	is_reported BOOLEAN DEFAULT false,
	is_edited BOOLEAN DEFAULT false,
	date_edited timestamptz
);

CREATE TABLE IF NOT EXISTS comment_table(
	comment_id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
	post_id uuid REFERENCES post_table,
	username VARCHAR(256) REFERENCES user_table,
	content TEXT,
	date_created timestamptz
);

CREATE TABLE IF NOT EXISTS vote_table(
	vote_id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
	post_id uuid REFERENCES post_table,
	username VARCHAR(256) REFERENCES user_table,
	direction INT NOT NULL,
	date_created timestamptz NOT NULL,
	date_changed timestamptz
);