INSERT INTO "Users"
    (
    "UserName",
    "UserPassword",
    "Email",
    "ValidationCode",
    "IsValidated",
    "DateCreated"
    )
VALUES
    ('admin', 'password', 'test@gmail.com', '1234', 'true', NOW());

INSERT INTO "Users"
    (
    "UserName",
    "UserPassword",
    "Email",
    "ValidationCode",
    "IsValidated",
    "DateCreated"
    )
VALUES
    ('steventt07', 'password', 'test1@gmail.com', '1234', 'true', NOW());

INSERT INTO "CategoryType"
    (
    "CategoryTypeDescription"
    )
VALUES
    ('Main Categories');

INSERT INTO "Category"
    (
    "CategoryTypeID",
    "CategoryTitle",
    "CategoryDescription",
    "DateCreated"
    )
VALUES
    (1, 'Deals', '', NOW());

INSERT INTO "Category"
    (
    "CategoryTypeID",
    "CategoryTitle",
    "CategoryDescription",
    "DateCreated"
    )
VALUES
    (1, 'Happy Hour', '', NOW());

INSERT INTO "Category"
    (
    "CategoryTypeID",
    "CategoryTitle",
    "CategoryDescription",
    "DateCreated"
    )
VALUES
    (1, 'Recreation', '', NOW());

INSERT INTO "Category"
    (
    "CategoryTypeID",
    "CategoryTitle",
    "CategoryDescription",
    "DateCreated"
    )
VALUES
    (1, 'What''s happening?', '', NOW());

INSERT INTO "Category"
    (
    "CategoryTypeID",
    "CategoryTitle",
    "CategoryDescription",
    "DateCreated"
    )
VALUES
    (1, 'Misc', '', NOW());

INSERT INTO "Post"
    (
    "UserID",
    "CategoryID",
    "PostTitle",
    "PostContent",
    "Latitude",
    "Longitude",
    "DateCreated"
    )
VALUES
    (1, 2, 'HEB', 'My first post', '10.2', '50.9', NOW());

INSERT INTO "Post"
    (
    "UserID",
    "CategoryID",
    "PostTitle",
    "PostContent",
    "Latitude",
    "Longitude",
    "DateCreated"
    )
VALUES
    (1, 2, 'Target', 'Huge jeans sale at target', '10.2', '50.9', NOW());

INSERT INTO "Post"
    (
    "UserID",
    "CategoryID",
    "PostTitle",
    "PostContent",
    "Latitude",
    "Longitude",
    "DateCreated"
    )
VALUES
    (1, 2, 'HEB', 'Steak is $7/lbs at HEB off Parmer', '10.2', '50.9', NOW());

INSERT INTO "Post"
    (
    "UserID",
    "CategoryID",
    "PostTitle",
    "PostContent",
    "Latitude",
    "Longitude",
    "DateCreated"
    )
VALUES
    (1, 2, 'Hopdoddy', 'Happy at Hopdoddy, $5 for drinks', '10.2', '50.9', NOW());

INSERT INTO "Post"
    (
    "UserID",
    "CategoryID",
    "PostTitle",
    "PostContent",
    "Latitude",
    "Longitude",
    "DateCreated"
    )
VALUES
    (1, 1, '35 and Palmer', 'Did yall see the crash on 35 and Parmer', '10.2', '50.9', NOW());

INSERT INTO "Post"
    (
    "UserID",
    "CategoryID",
    "PostTitle",
    "PostContent",
    "Latitude",
    "Longitude",
    "DateCreated"
    )
VALUES
    (1, 1, 'Downtown', 'Shooting downtown, stay safe ', '10.2', '50.9', NOW());

INSERT INTO "Post"
    (
    "UserID",
    "CategoryID",
    "PostTitle",
    "PostContent",
    "Latitude",
    "Longitude",
    "DateCreated"
    )
VALUES
    (1, 1, '6th', 'Epic rager on 6th', '10.2', '50.9', NOW());

INSERT INTO "Post"
    (
    "UserID",
    "CategoryID",
    "PostTitle",
    "PostContent",
    "Latitude",
    "Longitude",
    "DateCreated"
    )
VALUES
    (1, 1, 'REI', 'There is a huge line at REI (Lamar)', '10.2', '50.9', NOW());

INSERT INTO "Post"
    (
    "UserID",
    "CategoryID",
    "PostTitle",
    "PostContent",
    "Latitude",
    "Longitude",
    "DateCreated"
    )
VALUES
    (1, 3, 'Moontower', 'Volleyball tournament next friday “sign up link', '10.2', '50.9', NOW());

INSERT INTO "Post"
    (
    "UserID",
    "CategoryID",
    "PostTitle",
    "PostContent",
    "Latitude",
    "Longitude",
    "DateCreated"
    )
VALUES
    (1, 3, 'rooftop', 'Pick up basketball @rooftop ', '10.2', '50.9', NOW());

INSERT INTO "Post"
    (
    "UserID",
    "CategoryID",
    "PostTitle",
    "PostContent",
    "Latitude",
    "Longitude",
    "DateCreated"
    )
VALUES
    (1, 3, 'Ladybird Lake', 'Paddle board place at Austin High School is open', '10.2', '50.9', NOW());

INSERT INTO "Post"
    (
    "UserID",
    "CategoryID",
    "PostTitle",
    "PostContent",
    "Latitude",
    "Longitude",
    "DateCreated"
    )
VALUES
    (1, 3, 'Austin High', 'Tennis courts at Austin High School is open', '10.2', '50.9', NOW());