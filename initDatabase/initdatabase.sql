-- Database: STUDPOSTS

-- DROP DATABASE IF EXISTS "STUDPOSTS";

    CREATE DATABASE "STUDPOSTS"
        WITH
        OWNER = postgres
        ENCODING = 'UTF8'
        LC_COLLATE = 'Russian_Russia.1251'
        LC_CTYPE = 'Russian_Russia.1251'
        LOCALE_PROVIDER = 'libc'
        TABLESPACE = pg_default
        CONNECTION LIMIT = -1
        IS_TEMPLATE = False;

    CREATE TABLE IF NOT EXISTS users (
        login VARCHAR(255) PRIMARY KEY,
        password VARCHAR(128) NOT NULL,
        firstName VARCHAR(50) NOT NULL,
        surName VARCHAR(50) NOT NULL,
        middleName VARCHAR(50),
        privileged BOOLEAN DEFAULT FALSE,
        email VARCHAR(36),
        phoneNumber VARCHAR(20),
        persPhotoData VARCHAR(255)
    );

    CREATE TABLE IF NOT EXISTS posts (
        unique_id VARCHAR(50) PRIMARY KEY,
        owner_login VARCHAR(255) NOT NULL,
        title VARCHAR(200) NOT NULL,
        content TEXT NOT NULL,
        tags VARCHAR(200),
        createdAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        imageData VARCHAR(255),
        viewCount INTEGER DEFAULT 0,
        likesCount INTEGER DEFAULT 0,
        dislikesCount INTEGER DEFAULT 0,
        FOREIGN KEY (owner_login) REFERENCES users (login)
    );

    CREATE TABLE IF NOT EXISTS comments (
        unique_id VARCHAR(50) PRIMARY KEY,
        owner_login VARCHAR(255) NOT NULL,
        post_id VARCHAR(50) NOT NULL,
        content TEXT NOT NULL,
        createdAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (owner_login) REFERENCES users (login),
        FOREIGN KEY (post_id) REFERENCES posts (unique_id)
    );
