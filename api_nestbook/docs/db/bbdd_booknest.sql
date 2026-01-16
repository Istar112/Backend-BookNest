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
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) UNIQUE,
    name VARCHAR(255),
    password VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    phone VARCHAR(15)
);

-- =========================================
-- BOOK
-- =========================================
CREATE TABLE IF NOT EXISTS book (
    id INT PRIMARY KEY AUTO_INCREMENT,
    isbn CHAR(13) UNIQUE KEY,
    title VARCHAR(255) NOT NULL,
    category VARCHAR(50),
    total_pages INT CHECK (total_pages >= 0),
    publication_date DATE,
    purchased BOOLEAN DEFAULT FALSE,
    cover_image VARCHAR(255)
);

-- =========================================
-- AUTHOR
-- =========================================
CREATE TABLE IF NOT EXISTS author (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name_author VARCHAR(255) NOT NULL,
    country VARCHAR(100),
    image VARCHAR(255)
);

-- =========================================
-- STATUS (desired, process, finished)
-- =========================================
CREATE TABLE IF NOT EXISTS status (
    id INT AUTO_INCREMENT PRIMARY KEY
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
    id_book INT,
    id_editorial INT,
    PRIMARY KEY (id),
    FOREIGN KEY (id_book) REFERENCES book (id) ON DELETE CASCADE,
    FOREIGN KEY (id_editorial) REFERENCES editorial (id) ON DELETE CASCADE,
    CONSTRAINT c_book_editorial UNIQUE (id_book, id_editorial)
);


-- =========================================
-- USER-READING RELATIONSHIP
-- =========================================
CREATE TABLE IF NOT EXISTS reading (
    id INT AUTO_INCREMENT,
    id_user INT,
    id_book INT,
    reading_status VARCHAR(255),
    id_status INT,
    PRIMARY KEY (id),
    FOREIGN KEY (id_user) REFERENCES user (id) ON DELETE CASCADE,
    FOREIGN KEY (id_book) REFERENCES book (id) ON DELETE CASCADE,
    FOREIGN KEY (id_status) REFERENCES status (id) ON DELETE CASCADE,
    CONSTRAINT c_user_book UNIQUE (id_user,id_book)
);

-- =========================================
-- BOOK-AUTHOR RELATIONSHIP
-- =========================================
CREATE TABLE IF NOT EXISTS book_author (
    id INT AUTO_INCREMENT,
    id_book INT,
    id_author INT,
    PRIMARY KEY (id),
    FOREIGN KEY (id_book) REFERENCES book (id) ON DELETE CASCADE,
    FOREIGN KEY (id_author) REFERENCES author (id) ON DELETE CASCADE,
    CONSTRAINT c_book_author UNIQUE (id_book, id_author)
);

-- ========================================
-- STATUS
-- ========================================
CREATE TABLE IF NOT EXISTS finished (
    id INT,
    finish_date DATE NOT NULL,
    rating VARCHAR(255),
    PRIMARY KEY (id),
    FOREIGN KEY (id) REFERENCES status (id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS process (
    id INT,
    num_pag INT NOT NULL,
    date_start DATE NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (id) REFERENCES status (id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS desired (
    id INT,
    comment VARCHAR(255),
    PRIMARY KEY (id),
    FOREIGN KEY (id) REFERENCES status (id) ON DELETE CASCADE
);


-- 2025-10-15 14:57:25 UTC
