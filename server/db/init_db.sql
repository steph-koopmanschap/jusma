-- Use this file to initialize the PostGreSQL database only once, before starting the server for the first time.

-- Create the database
CREATE DATABASE jasma_db
    WITH
    OWNER = postgres
    TEMPLATE = template0
    ENCODING = 'UTF8'
    LC_COLLATE = 'en_US.UTF-8'
    LC_CTYPE = 'en_US.UTF-8'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1
    IS_TEMPLATE = False;

COMMENT ON DATABASE jasma_db
    IS 'The Database for the JASMA App';

-- Connect to the newly created database as current user
\c jasma_db

-- Drop tables first in case something is wrong
DROP TABLE IF EXISTS transactions;
DROP TABLE IF EXISTS ads_preferences;
DROP TABLE IF EXISTS ads;
DROP TABLE IF EXISTS comments;
DROP TABLE IF EXISTS posts_hashtags;
DROP TABLE IF EXISTS hashtags;
DROP TABLE IF EXISTS posts_metadata;
DROP TABLE IF EXISTS posts;
DROP TABLE IF EXISTS users_following;
DROP TABLE IF EXISTS users_preferences;
DROP TABLE IF EXISTS users_metadata;
DROP TABLE IF EXISTS users_info;
DROP TABLE IF EXISTS users;

-- Create the tables
-- some column names have table name in front of them to prevent using SQL keywords
-- For a list of SQL keywords see: https://www.postgresql.org/docs/current/sql-keywords-appendix.html
-- UUIDs are generated by the server, not in PSQL.
-- Note the user_password is a HASH made out of exactly 60 characters. It does not store plaintext characters
CREATE TABLE IF NOT EXISTS users(
    user_id         UUID PRIMARY KEY,
    username        VARCHAR(25) UNIQUE NOT NULL,
    email           VARCHAR(50) UNIQUE NOT NULL,
    recovery_email  VARCHAR(50),
    user_password   CHAR(60) NOT NULL,
    phone           VARCHAR(20),
    recovery_phone  VARCHAR(20)
);

-- Create indexes for faster querying on usernames (the primary way to retrieve data)
CREATE INDEX users_username_idx ON users (username);
CREATE INDEX users_email_idx ON users (email);

-- One to one relationship with table users
-- by default the user's display name is their username,
-- but they can also use their given_name or last_name if they prefer.
CREATE TABLE IF NOT EXISTS users_info(
    user_id         UUID REFERENCES users(user_id) ON DELETE CASCADE UNIQUE NOT NULL,
    profile_pic     BYTEA,
    given_name      VARCHAR(35),
    last_name       VARCHAR(35),
    bio             TEXT, 
    date_of_birth   DATE,
    country         TEXT,
    city            TEXT,
    website         TEXT,
    PRIMARY KEY (user_id)
);

-- One to one relationship with table users
CREATE TABLE IF NOT EXISTS users_metadata(
    user_id               UUID REFERENCES users(user_id) ON DELETE CASCADE UNIQUE NOT NULL,           
    user_role             VARCHAR(10) NOT NULL
        CHECK(user_role IN ('guest', 'normal', 'mod', 'admin')),
    last_login_date       DATE NOT NULL,
    account_creation_date DATE NOT NULL,
    isVerified_email      BOOLEAN NOT NULL,
    last_ipv4             VARCHAR(55),
    PRIMARY KEY (user_id)
);

-- One to one relationship with table users
CREATE TABLE IF NOT EXISTS users_preferences(
    user_id             UUID REFERENCES users(user_id) ON DELETE CASCADE UNIQUE NOT NULL,           
    email_notifications BOOLEAN NOT NULL,
    PRIMARY KEY (user_id)
);

-- Not sure if this works? 
-- should they be composite primary key??
CREATE TABLE IF NOT EXISTS users_following(
    user_id             UUID REFERENCES users(user_id) ON DELETE CASCADE NOT NULL,
    follow_id           UUID REFERENCES users(user_id) ON DELETE CASCADE NOT NULL
);

-- One to many relationship with table users
CREATE TABLE IF NOT EXISTS posts(
    post_id         UUID UNIQUE NOT NULL,
    user_id         UUID REFERENCES users(user_id),
    text_content    TEXT NOT NULL,
    file_content    BYTEA,
    created_at      TIMESTAMP NOT NULL,
    last_edit_at    TIMESTAMP NOT NULL,
    PRIMARY KEY (post_id, user_id)
);

-- One to one relationship with table posts
-- Not sure if this table is still needed?
CREATE TABLE IF NOT EXISTS posts_metadata(
    post_id             UUID REFERENCES posts(post_id) ON DELETE CASCADE UNIQUE NOT NULL,
    PRIMARY KEY (post_id)
);

CREATE TABLE IF NOT EXISTS hashtags(
    hashtag         VARCHAR(50) PRIMARY KEY
);

-- Many to many relationship with posts and hashtags
CREATE TABLE IF NOT EXISTS posts_hashtags(
    post_id         UUID REFERENCES posts(post_id) ON DELETE CASCADE,
    hashtag         VARCHAR(50) REFERENCES hashtags(hashtag),
    PRIMARY KEY (post_id, hashtag)
);

-- One to many relationship with posts
CREATE TABLE IF NOT EXISTS comments(
    comment_id      UUID PRIMARY KEY,
    post_id         UUID REFERENCES posts(post_id) ON DELETE CASCADE,
    user_id         UUID REFERENCES users(user_id),
    comment_text    TEXT NOT NULL,
    comment_file    BYTEA,
    created_at      TIMESTAMP NOT NULL
);

-- One to many relationship with users
CREATE TABLE IF NOT EXISTS ads(
    ad_id           UUID PRIMARY KEY,
    user_id         UUID REFERENCES users(user_id) ON DELETE CASCADE,
    ad_file         BYTEA NOT NULL,
    ad_url          TEXT
    created_at      TIMESTAMP NOT NULL,
    expires_at      TIMESTAMP NOT NULL
);

-- One to one relationship with ads
-- Used for targeting demographics with ads
CREATE TABLE IF NOT EXISTS ads_preferences(
    ad_id           UUID REFERENCES ads(ad_id) UNIQUE ON DELETE CASCADE,
    age_start       SMALLINT,
    age_end         SMALLINT,
    country         TEXT,
    city            TEXT,
    keyword         VARCHAR(50)
);

-- One to many relationship with users
-- ad_id is not an FK of ads, because ads are deleted, but transactions are permanent
CREATE TABLE IF NOT EXISTS transactions(
    transaction_id   UUID PRIMARY KEY,
    user_id          UUID REFERENCES users(user_id),
    ad_id            UUID
    transaction_date TIMESTAMP NOT NULL,
    price            MONEY NOT NULL,
    payment_method   VARCHAR(50)
);

CREATE ROLE jasma_admin LOGIN PASSWORD 'a';

-- Grant full permissions on the database
GRANT ALL PRIVILEGES ON DATABASE jasma_db TO jasma_admin;
GRANT ALL PRIVILEGES ON SCHEMA public TO jasma_admin;
GRANT ALL PRIVILEGES ON ALL TABLES    IN SCHEMA public to jasma_admin;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public to jasma_admin;
GRANT ALL PRIVILEGES ON ALL FUNCTIONS IN SCHEMA public to jasma_admin;
ALTER DATABASE jasma_db OWNER TO jasma_admin;

-- +++++++++++++++++++++++++++++++++++++++++++++++++++++

-- Create a default "NULL" or "Guest" user which equals non-logged in users
-- password = guest
INSERT INTO users(user_id, username, email, recovery_email, user_password, phone, recovery_phone)
VALUES(
    uuid('00000000-0000-0000-0000-000000000000'),
    'guest',
    'guest@jasma.com',
    'guest@jasma.com',
    '$2b$10$IBxqRMTBqrmxhGFnYPEPTOMbHWEj/VY7Glzd0f7ttfkeAYrwM5tES',
    '0123456789',
    '0123456789'
);

INSERT INTO users_info(user_id)
VALUES(
    uuid('00000000-0000-0000-0000-000000000000')
);

INSERT INTO users_metadata(user_id, user_role, last_login_date, account_creation_date, isVerified_email)
VALUES(
    uuid('00000000-0000-0000-0000-000000000000'),
    'guest',
    TO_DATE('2000-01-01', 'YYYY-MM-DD'),
    TO_DATE('2000-01-01', 'YYYY-MM-DD'),
    FALSE
);

INSERT INTO users_preferences(user_id, email_notifications)
VALUES(
    uuid('00000000-0000-0000-0000-000000000000'),
    FALSE
);
