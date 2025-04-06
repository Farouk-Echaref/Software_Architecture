-- create a database-level user who can access the DB from localhost only

CREATE USER 'auth_user'@'localhost' IDENTIFIED BY 'Auth123';

-- create DB where the app will store authentication data

CREATE DATABASE auth;

-- Gives full access (ALL PRIVILEGES) to auth_user on all tables inside the auth database.
-- Now auth_user can create tables, insert data, update, etc., within this specific database.

GRANT ALL PRIVILEGES ON auth.* TO 'auth_user'@'localhost';

-- Switches the context so that subsequent operations apply to the auth database

USE auth;

-- create a user table to store new users and their passwords

CREATE TABLE user (
    -- primary key with a unique integer for each user
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL
);


-- insert a sample user, this is the user that will interact with our app
-- this is for learning purposes, the password should be hashed
-- this user will have access to our Gateway API

INSERT INTO user (email, password) VALUES ('farouk.echcharef20@gmail.com', 'Admin123');