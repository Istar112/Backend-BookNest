-- Adminer 5.4.0 MariaDB 12.0.2-MariaDB-ubu2404 dump
-- @autor Víctor Manuel Ferrández Ballester, Istar Hernández Fernández
-- @version v0.0.1

-- port: 8019
-- user: root
-- passw: root
-- Enter, import bbdd_booknest.sql and execute.
-- Finally select the database created.

-- CREATE DATABASE IF NOT EXISTS bbdd_booknest;
-- USE bbdd_booknest;
-- =========================================
-- USUARIO
-- =========================================
CREATE TABLE IF NOT EXISTS user (
    username VARCHAR(50) PRIMARY KEY,
    name VARCHAR(255),
    password VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    phone VARCHAR(15)
);

-- =========================================
-- BOOK
-- =========================================
CREATE TABLE IF NOT EXISTS book (
    isbn CHAR(13) PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    category VARCHAR(50),
    total_pages INT CHECK (total_pages >= 0),
    publication_date DATE,
    purchased BOOLEAN DEFAULT FALSE
);

-- =========================================
-- AUTHOR
-- =========================================
CREATE TABLE IF NOT EXISTS author (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name_author VARCHAR(255) NOT NULL,
    country VARCHAR(100)
);

-- =========================================
-- STATUS (desired, process, finished)
-- =========================================
CREATE TABLE IF NOT EXISTS status (
    id INT AUTO_INCREMENT PRIMARY KEY,
    category VARCHAR(50)
);

-- =========================================
-- EDITORIAL
-- =========================================
CREATE TABLE IF NOT EXISTS editorial (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name_editorial VARCHAR(255) NOT NULL
);

-- =========================================
-- BOOK-EDITORIAL RELATIONSHIP
-- =========================================
CREATE TABLE IF NOT EXISTS book_editorial (
    id INT AUTO_INCREMENT,
    isbn_book CHAR(13),
    id_editorial INT,
    PRIMARY KEY (id),
    FOREIGN KEY (isbn_book) REFERENCES book (isbn) ON DELETE CASCADE,
    FOREIGN KEY (id_editorial) REFERENCES editorial (id) ON DELETE CASCADE,
    CONSTRAINT c_book_editorial UNIQUE (isbn_book, id_editorial)
);


-- =========================================
-- USER-READING RELATIONSHIP
-- =========================================
CREATE TABLE IF NOT EXISTS reading (
    id INT AUTO_INCREMENT,
    username VARCHAR(255),
    isbn CHAR(13),
    reading_status VARCHAR(255),
    id_condition INT,
    PRIMARY KEY (id),
    FOREIGN KEY (username) REFERENCES user (username) ON DELETE CASCADE,
    FOREIGN KEY (isbn) REFERENCES book (isbn) ON DELETE CASCADE,
    CONSTRAINT c_username_isbn UNIQUE (username, isbn)
);

-- =========================================
-- BOOK-AUTHOR RELATIONSHIP
-- =========================================
CREATE TABLE IF NOT EXISTS book_author (
    id INT AUTO_INCREMENT,
    isbn_book CHAR(13),
    id_author INT,
    PRIMARY KEY (id),
    FOREIGN KEY (isbn_book) REFERENCES book (isbn) ON DELETE CASCADE,
    FOREIGN KEY (id_author) REFERENCES author (id) ON DELETE CASCADE,
    CONSTRAINT c_book_author UNIQUE (isbn_book, id_author)
);

-- ========================================
-- STATUS
-- ========================================
CREATE TABLE IF NOT EXISTS finished (
    id INT AUTO_INCREMENT,
    finish_date DATE NOT NULL,
    rating VARCHAR(255),
    PRIMARY KEY (id),
    FOREIGN KEY (id) REFERENCES status (id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS process (
    id INT AUTO_INCREMENT,
    num_pag INT NOT NULL,
    date_start DATE NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (id) REFERENCES status (id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS desired (
    id INT AUTO_INCREMENT,
    PRIMARY KEY (id),
    FOREIGN KEY (id) REFERENCES status (id) ON DELETE CASCADE
);


-- 2025-10-15 14:57:25 UTC
