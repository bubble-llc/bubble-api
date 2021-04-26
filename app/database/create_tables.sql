CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "citext";
CREATE EXTENSION IF NOT EXISTS "postgis";
/* 
	I added Category Type so that if you wanted to do a report and group categories, this would be an 
	easy way to do that.  If not, can always remove table and foreign key
*/
CREATE TABLE IF NOT EXISTS "CategoryType"(
	"CategoryTypeID" SMALLSERIAL PRIMARY KEY,
	"CategoryTypeDescription" VARCHAR(256),
	"IsActive" BOOLEAN DEFAULT true
);
COMMENT ON COLUMN "CategoryType"."CategoryTypeDescription" is 'Description of a type of category';
COMMENT ON COLUMN "CategoryType"."IsActive" is 'Flag uses to turn on and off category types';

CREATE TABLE IF NOT EXISTS "UserType"(
	"UserTypeID" BIGSERIAL PRIMARY KEY,
	"UserTypeName" CITEXT NOT NULL UNIQUE,
	"IsActive" BOOLEAN DEFAULT true
);

CREATE TABLE IF NOT EXISTS "Users"(
	"UserID" BIGSERIAL PRIMARY KEY,
	"UserKey" UUID NOT NULL DEFAULT uuid_generate_v4(),
	"UserTypeID" BIGINT REFERENCES "UserType",
	"UserName" CITEXT NOT NULL UNIQUE,
	"UserPassword" VARCHAR(256) NOT NULL,
	"Email" VARCHAR(256) NOT NULL UNIQUE,
	"IsActive" BOOLEAN DEFAULT false,
	"IsValidated" BOOLEAN DEFAULT false,
	"IsLocked" BOOLEAN DEFAULT false,
	"ValidationCode" VARCHAR(256) NOT NULL,
	"PasswordValidationCode" VARCHAR(256),
	"SMSValidationCode" VARCHAR(256),
	"DateCreated" timestamptz,
	"DateValidated" timestamptz,
	"DateLocked" timestamptz,
	"LoggedInCount" INT DEFAULT(0),
	"FailedAttemptCount" INT DEFAULT(0),
	"DefaultCategoryID" INT DEFAULT(1) REFERENCES "Category"
);
COMMENT ON COLUMN "Users"."UserKey" is 'Key used for external selection of user';
COMMENT ON COLUMN "Users"."UserName" is 'Username for user';
COMMENT ON COLUMN "Users"."UserPassword" is 'Password for user';
COMMENT ON COLUMN "Users"."Email" is 'Email for user';
COMMENT ON COLUMN "Users"."IsActive" is 'Is user active';
COMMENT ON COLUMN "Users"."IsValidated" is 'Did user validate email';
COMMENT ON COLUMN "Users"."IsLocked" is 'Is user account locked';
COMMENT ON COLUMN "Users"."ValidationCode" is 'Code used for user to validate signup';

CREATE TABLE IF NOT EXISTS "Category"(
	"CategoryID" SERIAL PRIMARY KEY,
	"CategoryTypeID" SMALLSERIAL REFERENCES "CategoryType",
	"CategoryTitle" VARCHAR(256),
	"CategoryDescription" VARCHAR(256),
	"IsActive" BOOLEAN DEFAULT true,
	"DateCreated" timestamptz
);
COMMENT ON COLUMN "Category"."CategoryTitle" is 'Title or name of a category';
COMMENT ON COLUMN "Category"."CategoryDescription" is 'Description of a category';
COMMENT ON COLUMN "Category"."IsActive" is 'Flag uses to turn on and off categories';

CREATE TABLE IF NOT EXISTS "Post"(
	"PostID" BIGSERIAL PRIMARY KEY,
	"PostKey" UUID NOT NULL DEFAULT uuid_generate_v4(),
	"UserID" BIGINT NOT NULL REFERENCES "Users",
	"CategoryID" INT REFERENCES "Category",
	"PostTitle" VARCHAR(256),
	"PostContent" TEXT,
	"Latitude" REAL,
	"Longitude" REAL,
	"DateCreated" timestamptz,
	"DateModified" timestamptz,
	"IsActive" BOOLEAN DEFAULT true,
	"IsReported" BOOLEAN DEFAULT false,
	"IsEdited" BOOLEAN DEFAULT false	
);

CREATE TABLE IF NOT EXISTS "PostComment"(
	"PostCommentID" BIGSERIAL PRIMARY KEY,
	"PostCommentKey" UUID NOT NULL DEFAULT uuid_generate_v4(),
	"ParentPostCommentID" BIGINT NULL REFERENCES "PostComment",
	"UserID" BIGINT REFERENCES "Users",
	"CommentContent" TEXT,
	"DateCreated" timestamptz,
	"IsActive" BOOLEAN DEFAULT true
);
/**
	1) The only comments allowed would be comments that had a null for ParentPostCommentID
	2) By building a cross ref table here, this allows a comment to a comment if you ever go down that path
	3) This model is tall, so with recursion, depending on pestgres limits, you can have that many branches, MS SQL 
	   is 32,767 branches, so I doubt you would ever get that far.
**/

CREATE TABLE IF NOT EXISTS "Post_PostComment"(
	"PostID" BIGINT,
	"PostCommentID" BIGINT,
	PRIMARY KEY ("PostID", "PostCommentID"),
    UNIQUE ("PostCommentID")
);
/**
	1) This is the same as your vote table
	2) No need to have voteID since it will not be referenced
	3) This model prevents a user to have more than 1 vote per post
**/

CREATE TABLE IF NOT EXISTS "Post_User"(
	"PostID" BIGINT REFERENCES "Post",
	"UserID" BIGINT REFERENCES "Users",
	"Direction" INT NOT NULL,
	"DateCreated" timestamptz NOT NULL,
	"DateModified" timestamptz
);

CREATE TABLE IF NOT EXISTS "Comment_User"(
	"PostCommentID" BIGINT REFERENCES "PostComment",
	"UserID" BIGINT REFERENCES "Users",
	"Direction" INT NOT NULL,
	"DateCreated" timestamptz NOT NULL,
	"DateModified" timestamptz
);

CREATE TABLE IF NOT EXISTS "PostReport"(
	"PostReportID" BIGSERIAL PRIMARY KEY,
	"PostReportKey" UUID NOT NULL DEFAULT uuid_generate_v4(),
	"ParentPostReportID" BIGINT NULL REFERENCES "PostReport",
	"UserID" BIGINT REFERENCES "Users",
	"ReportContent" TEXT,
	"DateCreated" timestamptz
);

CREATE TABLE IF NOT EXISTS "Post_PostReport"(
	"PostID" BIGINT,
	"PostReportID" BIGINT,
	PRIMARY KEY ("PostID", "PostReportID"),
    UNIQUE ("PostReportID")
);

CREATE TABLE IF NOT EXISTS "Feedback"(
	"FeedbackID" BIGSERIAL PRIMARY KEY,
	"UserID" BIGINT REFERENCES "Users",
	"UserCommentedID" BIGINT REFERENCES "Users",
	"FeedbackContent" TEXT,
	"FeedbackComment" TEXT,
	"Latitude" REAL,
	"Longitude" REAL,
    "IsActive" BOOLEAN DEFAULT true,
	"DateCreated" timestamptz NOT NULL,
	"DateModified" timestamptz
);

CREATE TABLE IF NOT EXISTS "TwilioLookup"(
	"SID" VARCHAR(256) PRIMARY KEY,
	"PhoneNumber" VARCHAR(256) UNIQUE,
	"IsActive" BOOLEAN DEFAULT true,
	"DateCreated" timestamptz NOT NULL,
	"DateModified" timestamptz
);