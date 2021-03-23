QUERY_CHECK_CONNECTION = """
    SELECT 1;
"""
# need to create a join for comments and make comments a json list

QUERY_GET_USER_LIKED_POST = """
	SELECT 
		"Post"."PostID",
		"Post"."UserID",
		"Post"."CategoryID",
		"Post"."PostTitle",
		"Post"."PostContent",
		"Post"."Latitude",
		"Post"."Longitude",
		CASE WHEN "Post_User"."Direction" is NULL THEN false ELSE true END AS "IsVoted",
		CASE WHEN "Post_User"."Direction" is NULL THEN 0 ELSE "Post_User"."Direction" END AS "PrevVote",
		"Post"."DateCreated",
		COALESCE(x.cnt,0) AS "Comments",
		COALESCE(y.cnt,0) AS "Votes",
		"Users"."UserName"
	FROM 
		"Post"
	INNER JOIN 
		"Post_User"
	ON 
		"Post"."PostID" = "Post_User"."PostID"
	LEFT JOIN 
		"Users" on "Users"."UserID" = "Post"."UserID"
	LEFT OUTER JOIN 
		(SELECT "PostID", count(*) cnt FROM "Post_PostComment" GROUP BY "PostID") x ON "Post"."PostID" = x."PostID"
	LEFT OUTER JOIN 
		(SELECT "PostID", SUM("Direction") cnt FROM "Post_User" GROUP BY "PostID") y ON "Post"."PostID" = y."PostID"
	WHERE "Post_User"."UserID" = %s AND "Post_User"."Direction" = 1
	ORDER BY
		"DateCreated" DESC;
"""

QUERY_GET_CATEGORY = """
	SELECT 
		"Post"."PostID",
		"Post"."UserID",
		"Post"."CategoryID",
		"Post"."PostTitle",
		"Post"."PostContent",
		"Post"."Latitude",
		"Post"."Longitude",
		CASE WHEN "Post_User"."Direction" is NULL THEN false ELSE true END AS "IsVoted",
		CASE WHEN "Post_User"."Direction" is NULL THEN 0 ELSE "Post_User"."Direction" END AS "PrevVote",
		"Post"."DateCreated",
		COALESCE(x.cnt,0) AS "Comments",
		COALESCE(y.cnt,0) AS "Votes",
		"Users"."UserName"
	FROM 
		"Post"
	LEFT JOIN 
		"Post_User" on "Post_User"."PostID" = "Post"."PostID" AND "Post_User"."UserID" = %s
	LEFT JOIN 
		"Users" on "Users"."UserID" = "Post"."UserID"
	LEFT OUTER JOIN 
		(SELECT "PostID", count(*) cnt FROM "Post_PostComment" GROUP BY "PostID") x ON "Post"."PostID" = x."PostID"
	LEFT OUTER JOIN 
		(SELECT "PostID", SUM("Direction") cnt FROM "Post_User" GROUP BY "PostID") y ON "Post"."PostID" = y."PostID"
	WHERE "Post"."CategoryID" = %s AND "Post"."IsActive" = true AND "Post"."IsReported" = false
	ORDER BY
		"DateCreated" DESC;
"""

QUERY_GET_DELETED_POST = """
	SELECT 
		"Post"."PostID",
		"Post"."UserID",
		"Post"."CategoryID",
		"Post"."PostTitle",
		"Post"."PostContent",
		"Post"."Latitude",
		"Post"."Longitude",
		CASE WHEN "Post_User"."Direction" is NULL THEN false ELSE true END AS "IsVoted",
		CASE WHEN "Post_User"."Direction" is NULL THEN 0 ELSE "Post_User"."Direction" END AS "PrevVote",
		"Post"."DateCreated",
		COALESCE(x.cnt,0) AS "Comments",
		COALESCE(y.cnt,0) AS "Votes",
		"Users"."UserName"
	FROM 
		"Post"
	LEFT JOIN 
		"Post_User" on "Post_User"."PostID" = "Post"."PostID" AND "Post_User"."UserID" = %s
	LEFT JOIN 
		"Users" on "Users"."UserID" = "Post"."UserID"
	LEFT OUTER JOIN 
		(SELECT "PostID", count(*) cnt FROM "Post_PostComment" GROUP BY "PostID") x ON "Post"."PostID" = x."PostID"
	LEFT OUTER JOIN 
		(SELECT "PostID", SUM("Direction") cnt FROM "Post_User" GROUP BY "PostID") y ON "Post"."PostID" = y."PostID"
	WHERE "Post"."IsActive" = false
	ORDER BY
		"DateCreated" DESC;
"""

QUERY_GET_REPORTED_POST = """
	SELECT 
		"Post"."PostID",
		"Post"."UserID",
		"Post"."CategoryID",
		"Post"."PostTitle",
		"Post"."PostContent",
		"Post"."Latitude",
		"Post"."Longitude",
		CASE WHEN "Post_User"."Direction" is NULL THEN false ELSE true END AS "IsVoted",
		CASE WHEN "Post_User"."Direction" is NULL THEN 0 ELSE "Post_User"."Direction" END AS "PrevVote",
		"Post"."DateCreated",
		COALESCE(x.cnt,0) AS "Comments",
		COALESCE(y.cnt,0) AS "Votes",
		"Users"."UserName"
	FROM 
		"Post"
	LEFT JOIN 
		"Post_User" on "Post_User"."PostID" = "Post"."PostID"
	LEFT JOIN 
		"Users" on "Users"."UserID" = "Post"."UserID"
	LEFT OUTER JOIN 
		(SELECT "PostID", count(*) cnt FROM "Post_PostComment" GROUP BY "PostID") x ON "Post"."PostID" = x."PostID"
	LEFT OUTER JOIN 
		(SELECT "PostID", SUM("Direction") cnt FROM "Post_User" GROUP BY "PostID") y ON "Post"."PostID" = x."PostID"
	WHERE "Post"."IsReported" = true
	ORDER BY
		"DateCreated" DESC;
"""

QUERY_GET_REPORTED_POST_REPORT = """
	SELECT 
		"Post"."PostID",
		"Post"."UserID",
		"Post"."CategoryID",
		"Post"."PostTitle",
		"Post"."PostContent",
		"Post"."Latitude",
		"Post"."Longitude",
		CASE WHEN "Post_User"."Direction" is NULL THEN false ELSE true END AS "IsVoted",
		CASE WHEN "Post_User"."Direction" is NULL THEN 0 ELSE "Post_User"."Direction" END AS "PrevVote",
		"Post"."DateCreated",
		COALESCE(x.cnt,0) AS "Comments",
		COALESCE(y.cnt,0) AS "Votes",
		"Users"."UserName"
	FROM 
		"Post"
	LEFT JOIN 
		"Post_User" on "Post_User"."PostID" = "Post"."PostID"
	LEFT JOIN 
		"Users" on "Users"."UserID" = "Post"."UserID"
	LEFT OUTER JOIN 
		(SELECT "PostID", count(*) cnt FROM "Post_PostComment" GROUP BY "PostID") x ON "Post"."PostID" = x."PostID"
	LEFT OUTER JOIN 
		(SELECT "PostID", SUM("Direction") cnt FROM "Post_User" GROUP BY "PostID") y ON "Post"."PostID" = x."PostID"
	WHERE "Post"."IsReported" = true
	ORDER BY
		"DateCreated" DESC;
"""

QUERY_GET_USER_CREATED_POST = """
	SELECT 
		"Post"."PostID",
		"Post"."UserID",
		"Post"."CategoryID",
		"Post"."PostTitle",
		"Post"."PostContent",
		"Post"."Latitude",
		"Post"."Longitude",
		CASE WHEN "Post_User"."Direction" is NULL THEN false ELSE true END AS "IsVoted",
		CASE WHEN "Post_User"."Direction" is NULL THEN 0 ELSE "Post_User"."Direction" END AS "PrevVote",
		"Post"."DateCreated",
		COALESCE(x.cnt,0) AS "Comments",
		COALESCE(y.cnt,0) AS "Votes",
		"Users"."UserName"
	FROM 
		"Post"
	LEFT JOIN 
		"Post_User" on "Post_User"."PostID" = "Post"."PostID" AND "Post_User"."UserID" = %s
	LEFT JOIN 
		"Users" on "Users"."UserID" = "Post"."UserID"
	LEFT OUTER JOIN 
		(SELECT "PostID", count(*) cnt FROM "Post_PostComment" GROUP BY "PostID") x ON "Post"."PostID" = x."PostID"
	LEFT OUTER JOIN 
		(SELECT "PostID", SUM("Direction") cnt FROM "Post_User" GROUP BY "PostID") y ON "Post"."PostID" = y."PostID"
	WHERE "Post"."UserID" = %s
	ORDER BY
		"DateCreated" DESC;
"""

QUERY_GET_USER = """
	SELECT
		"UserName",
		"UserID",
		"Email",
		"DateCreated"
	FROM
		"Users"
	WHERE 
		"UserName" = %s AND "UserPassword" = %s AND "IsValidated" = true;
		
"""

QUERY_GET_COMMENT = """
	SELECT
		pc."PostCommentID",
		pc."UserID",
		pc."CommentContent",
		pc."DateCreated",
		"Users"."UserName"
	FROM
		"Post" p
	INNER JOIN "Post_PostComment" ppc
		ON p."PostID" = ppc."PostID"
	INNER JOIN "PostComment" pc
		ON ppc."PostCommentID" = pc."PostCommentID"
	LEFT JOIN 
		"Users" on "Users"."UserID" = pc."UserID"
	WHERE
		p."PostID" = %s;
		
"""

QUERY_INSERT_POST_TO_CATEGORY = """
	INSERT INTO "Post"(
		"UserID",
		"CategoryID",
		"PostTitle",
		"PostContent",
		"Latitude",
		"Longitude",
		"DateCreated"
	)
	VALUES (%s, %s, %s, %s, %s, %s, %s);
"""

QUERY_INSERT_USER = """
	INSERT INTO "Users"(
		"UserName",
		"UserPassword",
		"Email",
		"ValidationCode",
		"DateCreated"
	)
	VALUES (%s, %s, %s, %s, %s);
"""

QUERY_REMOVE_POST_FROM_CATEGORY = """
	UPDATE 
		"Post"
	SET
		"IsActive" = true,
		"DateModified" = %s
	WHERE "PostID" = %s AND "CategoryID" = %s;
"""

QUERY_INSERT_VOTE = """
	INSERT INTO "Post_User"(
		"PostID",
		"UserID",
		"Direction",
		"DateCreated"
	)
	VALUES (%s, %s, %s, %s);
"""

QUERY_INSERT_FEEDBACK = """
	INSERT INTO "Feedback"(
		"UserID",
		"FeedbackContent",
		"Latitude",
		"Longitude",
		"DateCreated"
	)
	VALUES (%s, %s, %s, %s, %s);
"""

QUERY_GET_FEEDBACK = """
	SELECT
		"FeedbackID",
		"UserID",
		"UserCommentedID",
		"FeedbackContent",
		"FeedbackComment",
		"Latitude",
		"Longitude",
		"DateCreated",
		"DateModified"
	FROM
		"Feedback"
	WHERE
		"IsActive" = true
"""

QUERY_UPDATE_VOTE = """
	UPDATE 
		"Post_User"
	SET
		"Direction" = %s,
		"DateModified" = %s
	WHERE "PostID" = %s AND "UserID" = %s;
"""

QUERY_UPDATE_REPORT_POST = """
	DO $$
	DECLARE PostReportID bigint;
	BEGIN
	INSERT INTO "PostReport"(
			"UserID",
			"ReportContent",
			"DateCreated"
		)
		VALUES (%s, %s, %s)
		returning "PostReportID" INTO PostReportID;

	INSERT INTO "Post_PostReport"(
            "PostID",
            "PostReportID"
        )
        VALUES (%s, PostReportID);

	UPDATE 
		"Post"
	SET
		"IsReported" = true
	WHERE "PostID" = %s;
	END $$
"""

QUERY_UPDATE_EMAIL_VERIFICATION = """
	UPDATE 
		"Users"
	SET
		"IsValidated" = true
	WHERE "Email" = %s AND "ValidationCode" = %s;
"""

QUERY_INSERT_COMMENT = """
    DO $$
    DECLARE PostCommentID bigint;
    BEGIN
    INSERT INTO "PostComment"(
            "UserID",
            "CommentContent",
            "DateCreated"
        )
        VALUES (%s, %s, %s)
        returning "PostCommentID" INTO PostCommentID;

    INSERT INTO "Post_PostComment"(
            "PostID",
            "PostCommentID"
        )
        VALUES (%s, PostCommentID);
    END $$
"""