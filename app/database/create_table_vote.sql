CREATE TABLE IF NOT EXISTS vote_table(
	vote_id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
	post_id uuid REFERENCES post_table,
	username VARCHAR(256) REFERENCES user_table,
	direction INT NOT NULL,
	date_created timestamptz NOT NULL,
	date_changed timestamptz
);