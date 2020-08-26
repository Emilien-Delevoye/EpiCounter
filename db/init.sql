CREATE DATABASE epicounter_db;

\c epicounter_db;

CREATE TABLE count (
    id INTEGER NOT NULL,
    update INTEGER NOT NULL,
    room VARCHAR (200) NOT NULL,
    door VARCHAR (200) NOT NULL,
    total INTEGER NOT NULL,
    total_raw INTEGER,
    date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);