


-- Create the Config table
CREATE TABLE simple_command (
    id SERIAL PRIMARY KEY,
    name VARCHAR(120) UNIQUE NOT NULL,
    value VARCHAR(120) NOT NULL,
    description VARCHAR(120) NOT NULL
);

-- Insert initial data into the Config table
INSERT INTO simple_command (name, value, description) VALUES
    ('date', '6.2.1', 'a'),
    ('discord', 'abc', 'a'),
    ('website', 'https://futrolajki.pl/', 'a'),
    ('program', 'https://futrolajki.pl/', 'a');
