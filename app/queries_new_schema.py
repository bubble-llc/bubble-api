QUERY_CHECK_CONNECTION = """
    SELECT 1;
"""
# need to create a join for comments and make comments a json list

QUERY_GET_RADIUS = """
	SELECT 
		"Post"."PostID"
	FROM 
		"Post"
	WHERE ST_DWithin("Post"."Geom", ST_GeomFromText('POINT(%s %s)', 4326)::geography, %s) AND "Post"."IsActive" = true
"""

QUERY_GET_USER_LIKED_POST = """
	SELECT 
		p."PostID",
		p."UserID",
		p."CategoryID",
		p."PostTitle",
		p."PostContent",
		p."Latitude",
		p."Longitude",
		CASE WHEN pu."Direction" is NULL THEN false ELSE true END AS "IsVoted",
		CASE WHEN pu."Direction" is NULL THEN 0 ELSE pu."Direction" END AS "PrevVote",
		p."DateCreated",
		COALESCE(ppc.cnt,0) AS "Comments",
		COALESCE(puv.cnt,0) AS "Votes",
		u."UserName"
	FROM 
		"Post" p
	INNER JOIN "Post_User" pu
		ON p."PostID" = pu."PostID"
	LEFT JOIN "Users" u
		ON u."UserID" = p."UserID"
	LEFT OUTER JOIN 
		(SELECT "PostID", count(*) cnt FROM "Post_PostComment" GROUP BY "PostID") ppc ON p."PostID" = ppc."PostID"
	LEFT OUTER JOIN 
		(SELECT "PostID", SUM("Direction") cnt FROM "Post_User" GROUP BY "PostID") puv ON p."PostID" = puv."PostID"
	WHERE pu."UserID" = %s AND pu."Direction" = 1 AND p."IsActive" = true
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
		COALESCE(ppc.cnt,0) AS "Comments",
		COALESCE(puv.cnt,0) AS "Votes",
		"Users"."UserName"
	FROM 
		"Post"
	LEFT JOIN 
		"Post_User" on "Post_User"."PostID" = "Post"."PostID" AND "Post_User"."UserID" = %s
	LEFT JOIN 
		"Users" on "Users"."UserID" = "Post"."UserID"
	LEFT OUTER JOIN 
		(SELECT "PostID", count(*) cnt FROM "Post_PostComment" pcc INNER JOIN "PostComment" pc
		ON pcc."PostCommentID" = pc."PostCommentID" AND pc."IsActive" = true GROUP BY "PostID") ppc ON "Post"."PostID" = ppc."PostID"
	LEFT OUTER JOIN 
		(SELECT "PostID", SUM("Direction") cnt FROM "Post_User" GROUP BY "PostID") puv ON "Post"."PostID" = puv."PostID"
	WHERE "Post"."CategoryID" = %s AND "Post"."IsActive" = true AND "Post"."IsReported" = false AND "Post"."IsActive" = true AND "Post"."UserID" NOT IN (SELECT "BlockedUserID" FROM "BlockedUser" WHERE "UserID" = %s AND "IsActive" = true)
		AND ST_DWithin("Post"."Geom", ST_GeomFromText('POINT(%s %s)', 4326)::geography, %s)
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
		COALESCE(ppc.cnt,0) AS "Comments",
		COALESCE(puv.cnt,0) AS "Votes",
		"Users"."UserName"
	FROM 
		"Post"
	LEFT JOIN 
		"Post_User" on "Post_User"."PostID" = "Post"."PostID" AND "Post_User"."UserID" = %s
	LEFT JOIN 
		"Users" on "Users"."UserID" = "Post"."UserID"
	LEFT OUTER JOIN 
		(SELECT "PostID", count(*) cnt FROM "Post_PostComment" GROUP BY "PostID") ppc ON "Post"."PostID" = ppc."PostID"
	LEFT OUTER JOIN 
		(SELECT "PostID", SUM("Direction") cnt FROM "Post_User" GROUP BY "PostID") puv ON "Post"."PostID" = puv."PostID"
	WHERE "Post"."IsActive" = false
	ORDER BY
		"DateCreated" DESC;
"""

QUERY_GET_POST_REVIEW = """
	SELECT DISTINCT
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
		COALESCE(ppc.cnt,0) AS "Comments",
		COALESCE(puv.cnt,0) AS "Votes",
		"Users"."UserName"
	FROM 
		"Post"
	LEFT JOIN 
		"Post_User" on "Post_User"."PostID" = "Post"."PostID"
	LEFT JOIN 
		"Users" on "Users"."UserID" = "Post"."UserID"
	LEFT OUTER JOIN 
		(SELECT "PostID", count(*) cnt FROM "Post_PostComment" GROUP BY "PostID") ppc ON "Post"."PostID" = ppc."PostID"
	LEFT OUTER JOIN 
		(SELECT "PostID", SUM("Direction") cnt FROM "Post_User" GROUP BY "PostID") puv ON "Post"."PostID" = puv."PostID"
	WHERE "Post"."IsReported" = true
	ORDER BY
		"DateCreated" DESC;
"""

QUERY_GET_COMMENT_REVIEW = """
	SELECT
		pc."PostCommentID",
		pc."UserID",
		pc."CommentContent",
		pc."DateCreated",
		u."UserName",
		COALESCE(cuv.cnt,0) AS "Votes",
		CASE WHEN cu."Direction" is NULL THEN false ELSE true END AS "IsVoted",
		CASE WHEN cu."Direction" is NULL THEN 0 ELSE cu."Direction" END AS "PrevVote"
	FROM
		"PostComment" pc
	LEFT JOIN "Comment_User" cu
		ON pc."PostCommentID" = cu."PostCommentID"
	LEFT JOIN "Users" u
		ON u."UserID" = pc."UserID"
	LEFT OUTER JOIN 
		(SELECT "PostCommentID", SUM("Direction") cnt FROM "Comment_User" GROUP BY "PostCommentID") cuv ON pc."PostCommentID" = cuv."PostCommentID"
	WHERE
		pc."IsReported" = true
	ORDER BY
		pc."DateCreated" DESC;
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
		COALESCE(ppc.cnt,0) AS "Comments",
		COALESCE(puv.cnt,0) AS "Votes",
		"Users"."UserName"
	FROM 
		"Post"
	LEFT JOIN 
		"Post_User" on "Post_User"."PostID" = "Post"."PostID"
	LEFT JOIN 
		"Users" on "Users"."UserID" = "Post"."UserID"
	LEFT OUTER JOIN 
		(SELECT "PostID", count(*) cnt FROM "Post_PostComment" GROUP BY "PostID") ppc ON "Post"."PostID" = ppc."PostID"
	LEFT OUTER JOIN 
		(SELECT "PostID", SUM("Direction") cnt FROM "Post_User" GROUP BY "PostID") puv ON "Post"."PostID" = puv."PostID"
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
		COALESCE(ppc.cnt,0) AS "Comments",
		COALESCE(puv.cnt,0) AS "Votes",
		"Users"."UserName"
	FROM 
		"Post"
	LEFT JOIN 
		"Post_User" on "Post_User"."PostID" = "Post"."PostID" AND "Post_User"."UserID" = %s
	LEFT JOIN 
		"Users" on "Users"."UserID" = "Post"."UserID"
	LEFT OUTER JOIN 
		(SELECT "PostID", count(*) cnt FROM "Post_PostComment" pcc INNER JOIN "PostComment" pc
		ON pcc."PostCommentID" = pc."PostCommentID" AND pc."IsActive" = true GROUP BY "PostID") ppc ON "Post"."PostID" = ppc."PostID"
	LEFT OUTER JOIN 
		(SELECT "PostID", SUM("Direction") cnt FROM "Post_User" GROUP BY "PostID") puv ON "Post"."PostID" = puv."PostID"
	WHERE "Post"."UserID" = %s AND "Post"."IsActive" = true
	ORDER BY
		"DateCreated" DESC;
"""

QUERY_GET_USER = """
	SELECT
		"UserName",
		"UserID",
		"UserTypeID",
		"Email",
		"DateCreated",
		"DefaultCategoryID"
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
		u."UserName",
		COALESCE(cuv.cnt,0) AS "Votes",
		CASE WHEN cu."Direction" is NULL THEN false ELSE true END AS "IsVoted",
		CASE WHEN cu."Direction" is NULL THEN 0 ELSE cu."Direction" END AS "PrevVote"
	FROM
		"Post" p
	INNER JOIN "Post_PostComment" ppc
		ON p."PostID" = ppc."PostID"
	INNER JOIN "PostComment" pc
		ON ppc."PostCommentID" = pc."PostCommentID" AND pc."IsActive" = true
	LEFT JOIN "Comment_User" cu
		ON pc."PostCommentID" = cu."PostCommentID" AND "cu"."UserID" = %s
	LEFT JOIN "Users" u
		ON u."UserID" = pc."UserID"
	LEFT OUTER JOIN 
		(SELECT "PostCommentID", SUM("Direction") cnt FROM "Comment_User" GROUP BY "PostCommentID") cuv ON ppc."PostCommentID" = cuv."PostCommentID"
	WHERE
		p."PostID" = %s AND pc."UserID" NOT IN (SELECT "BlockedUserID" FROM "BlockedUser" WHERE "UserID" = %s AND "IsActive" = true)
	ORDER BY
		pc."DateCreated" ASC;
"""

QUERY_INSERT_POST_TO_CATEGORY = """
	INSERT INTO "Post"(
		"UserID",
		"CategoryID",
		"PostTitle",
		"PostContent",
		"Latitude",
		"Longitude",
		"DateCreated",
		"Geom"
	)
	VALUES (%s, %s, %s, %s, %s, %s, %s, ST_SetSRID(ST_MakePoint(%s, %s), 4326));
"""

QUERY_INSERT_USER = """
	INSERT INTO "Users"(
		"UserName",
		"UserTypeID",
		"UserPassword",
		"Email",
		"ValidationCode",
		"DateCreated"
	)
	VALUES (%s, %s, %s, %s, %s, %s);
"""

QUERY_REMOVE_POST_FROM_CATEGORY = """
	UPDATE 
		"Post"
	SET
		"IsActive" = true,
		"DateModified" = %s
	WHERE "PostID" = %s AND "CategoryID" = %s;
"""

QUERY_INSERT_POST_VOTE = """
	INSERT INTO "Post_User"(
		"PostID",
		"UserID",
		"Direction",
		"DateCreated"
	)
	VALUES (%s, %s, %s, %s);
"""

QUERY_UPDATE_POST_VOTE = """
	UPDATE 
		"Post_User"
	SET
		"Direction" = %s,
		"DateModified" = %s
	WHERE "PostID" = %s AND "UserID" = %s;
"""

QUERY_INSERT_COMMENT_VOTE = """
	INSERT INTO "Comment_User"(
		"PostCommentID",
		"UserID",
		"Direction",
		"DateCreated"
	)
	VALUES (%s, %s, %s, %s);
"""

QUERY_UPDATE_COMMENT_VOTE = """
	UPDATE 
		"Comment_User"
	SET
		"Direction" = %s,
		"DateModified" = %s
	WHERE "PostCommentID" = %s AND "UserID" = %s;
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

QUERY_UPDATE_POST_REVIEW = """
	BEGIN;
	INSERT INTO "PostContentReview"(
			"UserID",
			"ReviewContent",
			"DateCreated",
			"PostID"
		)
		VALUES (%s, %s, %s, %s);
	UPDATE 
		"Post"
	SET
		"IsReported" = true
	WHERE "PostID" = %s;
	END
"""

QUERY_UPDATE_COMMENT_REVIEW = """
	BEGIN;
	INSERT INTO "CommentContentReview"(
			"UserID",
			"ReviewContent",
			"DateCreated",
			"PostCommentID"
		)
		VALUES (%s, %s, %s, %s);
	UPDATE 
		"PostComment"
	SET
		"IsReported" = true
	WHERE "PostCommentID" = %s;
	END
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

QUERY_INSERT_PASSWORD_RESET = """
	UPDATE 
		"Users"
	SET
		"PasswordValidationCode" = %s
	WHERE "Email" = %s;
"""

QUERY_CHECK_PASSWORD_RECOVERY_CODE = """
	SELECT 
		u."Email"
	FROM 
		"Users" u
	WHERE u."Email" = %s AND "PasswordValidationCode" = %s;
"""

QUERY_UPDATE_PASSWORD_RESET = """
	UPDATE 
		"Users"
	SET
		"UserPassword" = %s
	WHERE "Email" = %s AND "PasswordValidationCode" = %s;
"""

QUERY_UPDATE_DEFAULT_CATEGORY = """
	UPDATE 
		"Users"
	SET
		"DefaultCategoryID" = %s
	WHERE "UserID" = %s;
"""

QUERY_UPDATE_USERNAME = """
	UPDATE 
		"Users"
	SET
		"UserName" = %s
	WHERE "UserID" = %s;
"""

QUERY_UPDATE_PASSWORD = """
	UPDATE 
		"Users"
	SET
		"UserPassword" = %s
	WHERE "UserID" = %s;
"""

QUERY_INSERT_TWILO_SMS = """
	INSERT INTO "TwilioLookup"(
		"SID",
		"PhoneNumber",
		"DateCreated"
	)
	VALUES (%s, %s, %s);
"""

QUERY_GET_TWILO_SMS = """
	SELECT
		"SID"
	FROM
		"TwilioLookup"
	WHERE
		"PhoneNumber" = %s
"""

QUERY_UPDATE_TWILO_SMS = """
	UPDATE 
		"TwilioLookup"
	SET
		"IsActive" = false
	WHERE
		"SID" = %s
"""

QUERY_GET_NOTIFCATIONS = """
	SELECT 
		n."NotificationID",
		n."NotifcationTypeID",
		n."NotifcationContent",
		n."DateCreated"

	FROM 
		"Notification" n
	WHERE n."IsViewed" = false AND "UserID" = %s
	ORDER BY
		n."DateCreated" DESC;
"""

QUERY_UPDATE_NOTIFCATIONS = """
	UPDATE 
		"Notification"
	SET
		"IsViewed" = true
	WHERE
		"NotificationID" = %s
"""

QUERY_INSERT_NOTIFCATIONS = """
	INSERT INTO "Notification"(
		"UserID",
		"NotifcationTypeID",
		"NotifcationContent",
		"DateCreated"
	)
	VALUES (%s, %s, %s, %s);
"""

QUERY_INSERT_BLOCK_USER = """
	INSERT INTO "BlockedUser"(
		"UserID",
		"BlockedUserID",
		"BlockedReason",
		"BlockedType",
		"DateCreated"
	)
	VALUES (%s, %s, %s, %s, %s)
	ON CONFLICT ("UserID","BlockedUserID") DO UPDATE SET "IsActive" = true;
"""

QUERY_UPDATE_UNBLOCK_USER = """
	UPDATE 
		"BlockedUser"
	SET
		"IsActive" = false,
		"DateModified" = %s
	WHERE
		"UserID" = %s AND "BlockedUserID" = %s
"""

QUERY_GET_BLOCK_USER = """
	SELECT 
		bu."BlockedUserID",
		bu."BlockedReason",
		bu."BlockedType",
		u."UserName"

	FROM 
		"BlockedUser" bu
	LEFT JOIN "Users" u
		ON u."UserID" = bu."BlockedUserID"
	WHERE bu."IsActive" = true AND bu."UserID" = %s
	ORDER BY
		bu."DateCreated" DESC;
"""

QUERY_GET_USERNAME = """
	SELECT 
		u."UserName"
	FROM 
		"Users" u
	WHERE u."UserName" = %s OR u."Email" = %s
"""

QUERY_GET_EMAIL = """
	SELECT 
		u."Email"
	FROM 
		"Users" u
	WHERE u."Email" = %s
"""

QUERY_DELETE_POST = """
	UPDATE 
		"Post"
	SET
		"IsActive" = false
	WHERE
		"PostID" = %s
"""

QUERY_DELETE_COMMENT = """
	UPDATE 
		"PostComment"
	SET
		"IsActive" = false
	WHERE
		"PostCommentID" = %s
"""