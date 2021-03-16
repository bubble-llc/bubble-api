-- QUERY_GET_CATEGORY
SELECT 
	post_id,
	username,
	category_name,
	content,
	comment_ids,
	votes,
	zipcode,
	date_created
FROM 
	post_table
WHERE category_name = 'What''s happening?' AND zipcode = '78703' AND is_deleted = false AND is_reported = false
ORDER BY
	date_created DESC;

-- QUERY_GET_FEED
SELECT 
	post_id,
	username,
	category_name,
	content,
	comment_ids,
	votes,
	zipcode,
	date_created
FROM 
	post_table
WHERE zipcode = '78703'
	AND is_deleted = false AND is_reported = false
ORDER BY
	date_created DESC;
	
-- QUERY_REMOVE_POST_FROM_CATEGORY
UPDATE 
	post_table
SET
	is_deleted = true,
	date_edited = '2020-08-12'
WHERE post_id = 3 AND category_name = 'What''s happening?'

-- QUERY_GET_DELETED_POST
SELECT 
	post_id,
	username,
	category_name,
	content,
	votes,
	zipcode,
	date_created
FROM 
	post_table
WHERE is_deleted = true
ORDER BY
	date_created DESC;
	
-- QUERY_GET_REPORTED_POST
SELECT 
	post_id,
	username,
	category_name,
	content,
	comment_ids,
	votes,
	zipcode,
	date_created
FROM 
	post_table
WHERE is_reported = true
ORDER BY
	date_created DESC;
	
	

SELECT 
		post_table.post_id,
		post_table.username,
		post_table.category_name,
		post_table.title,
		post_table.content,
		post_table.votes,
		CASE WHEN vote_table.direction is NULL THEN false ELSE true END AS is_voted,
		vote_table.direction,
		post_table.zipcode,
		post_table.date_created,
		post_table.comment_ids,
		COALESCE(x.cnt,0) AS comments
	FROM 
		post_table
	LEFT JOIN 
        vote_table on vote_table.post_id = post_table.post_id AND vote_table.username = 'steventt07'
	LEFT OUTER JOIN 
		(SELECT post_id, count(*) cnt FROM comment_table GROUP BY post_id) x ON post_table.post_id = x.post_id
	WHERE zipcode = '78703' AND is_deleted = false AND is_reported = false
	ORDER BY
		date_created DESC;