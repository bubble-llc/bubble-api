INSERT INTO user_table(
        username,
		password,
		email,
		validation_code,
		is_validated,
		date_joined
	)
VALUES ('admin', 'password', 'test@gmail.com', '1234', 'true', NOW());

INSERT INTO user_table(
        username,
		password,
		email,
		validation_code,
		is_validated,
		date_joined
	)
VALUES ('steventt07', 'password', 'test1@gmail.com', '1234', 'true',  NOW());

INSERT INTO category_table(
        category_name,
        owner_username,
        date_created
	)
VALUES ('What''s happening?', 'admin', NOW());

INSERT INTO category_table(
        category_name,
        owner_username,
        date_created
	)
VALUES ('Deals', 'admin', NOW());

INSERT INTO category_table(
        category_name,
        owner_username,
        date_created
	)
VALUES ('Misc', 'admin', NOW());

INSERT INTO category_table(
        category_name,
        owner_username,
        date_created
	)
VALUES ('Happy Hour', 'admin', NOW());

INSERT INTO category_table(
        category_name,
        owner_username,
        date_created
	)
VALUES ('Recreation', 'admin', NOW());

INSERT INTO post_table(
		username,
		category_name,
		title,
		content,
		latitude,
		longitude,
		date_created
	)
VALUES ('steventt07', 'Deals', 'HEB', 'My first post', '10.2', '50.9', NOW());

INSERT INTO post_table(
		username,
		category_name,
		title,
		content,
		latitude,
		longitude,
		date_created
	)
VALUES ('steventt07', 'Deals', '', 'Huge jeans sale at target', '10.2', '50.9', NOW());

INSERT INTO post_table(
		username,
		category_name,
		title,
		content,
		latitude,
		longitude,
		date_created
	)
VALUES ('steventt07', 'Deals', 'Steak!!!', 'Steak is $7/lbs at HEB off Parmer', '10.2', '50.9', NOW());

INSERT INTO post_table(
		username,
		category_name,
		title,
		content,
		latitude,
		longitude,
		date_created
	)
VALUES ('steventt07', 'Deals', 'Burger', 'Happy at Hopdoddy, $5 for drinks', '10.2', '50.9', NOW());

INSERT INTO post_table(
		username,
		category_name,
		title,
		content,
		latitude,
		longitude,
		date_created
	)
VALUES ('steventt07', 'What''s happening?', 'DEALS!!!', 'Did yall see the crash on 35 and Parmer', '10.2', '50.9', NOW());

INSERT INTO post_table(
		username,
		category_name,
		title,
		content,
		latitude,
		longitude,
		date_created
	)
VALUES ('steventt07', 'What''s happening?', '!!!', 'Shooting downtown, stay safe ', '10.2', '50.9', NOW());

INSERT INTO post_table(
		username,
		category_name,
		title,
		content,
		latitude,
		longitude,
		date_created
	)
VALUES ('steventt07', 'What''s happening?', 'DEA!!', 'Epic rager on 6th', '10.2', '50.9', NOW());

INSERT INTO post_table(
		username,
		category_name,
		title,
		content,
		latitude,
		longitude,
		date_created
	)
VALUES ('steventt07', 'What''s happening?', '!!', 'There is a huge line at REI (Lamar)', '10.2', '50.9', NOW());

INSERT INTO post_table(
		username,
		category_name,
		title,
		content,
		latitude,
		longitude,
		date_created
	)
VALUES ('steventt07', 'Recreation', 'DEAL!', 'Volleyball tournament next friday “sign up link”', '10.2', '50.9', NOW());

INSERT INTO post_table(
		username,
		category_name,
		title,
		content,
		latitude,
		longitude,
		date_created
	)
VALUES ('steventt07', 'Recreation', 'DES!!!', 'Pick up basketball @rooftop ', '10.2', '50.9', NOW());

INSERT INTO post_table(
		username,
		category_name,
		title,
		content,
		latitude,
		longitude,
		date_created
	)
VALUES ('steventt07', 'Recreation', 'LS!!!', 'Paddle board place at Austin High School is open', '10.2', '50.9', NOW());

INSERT INTO post_table(
		username,
		category_name,
		title,
		content,
		latitude,
		longitude,
		date_created
	)
VALUES ('steventt07', 'Recreation', 'EALS!!!', 'Tennis courts at Austin High School is open', '10.2', '50.9', NOW());