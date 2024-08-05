create database rkive;
USE rkive;
show databases;
select * from accounts;

CREATE TABLE accounts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(100) NOT NULL
);

CREATE TABLE photos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    filename VARCHAR(255) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES accounts(id)
);

CREATE TABLE followers (
    follower_id INT NOT NULL,
    followee_id INT NOT NULL,
    PRIMARY KEY (follower_id, followee_id),
    FOREIGN KEY (follower_id) REFERENCES accounts(id) ON DELETE CASCADE,
    FOREIGN KEY (followee_id) REFERENCES accounts(id) ON DELETE CASCADE
);


