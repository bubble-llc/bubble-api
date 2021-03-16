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