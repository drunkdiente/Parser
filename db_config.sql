CREATE DATABASE IF NOT EXISTS hh_ru;
USE hh_ru;

CREATE TABLE IF NOT EXISTS vacancies (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    alternate_url VARCHAR(255),
    salary VARCHAR(255),
    employer VARCHAR(255),
    requirement TEXT
);
