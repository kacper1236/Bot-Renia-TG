-- Create the simple_command table
CREATE TABLE simple_command (
    id SERIAL PRIMARY KEY,
    name VARCHAR(120) UNIQUE NOT NULL,
    value VARCHAR(120) NOT NULL,
    description VARCHAR(120) NOT NULL
);

-- Insert initial data into the simple_command table
INSERT INTO simple_command (name, value, description) VALUES
    ('date', '6.2.1', 'a'),
    ('discord', 'abc', 'a'),
    ('website', 'https://futrolajki.pl/', 'a'),
    ('program', 'https://futrolajki.pl/', 'a');

-- Create the config table
CREATE TABLE config (
    id SERIAL PRIMARY KEY,
    name VARCHAR(120) UNIQUE NOT NULL,
    value VARCHAR(120) NOT NULL,
    description VARCHAR(120) NOT NULL
);

-- Insert initial data into the config table
INSERT INTO config (name, value, description) VALUES
    ('photo_upload', '0', '0 lub 1 w zaleznosci czy komendia /zdjecia do uploadowania zdjec ma byc aktywna');