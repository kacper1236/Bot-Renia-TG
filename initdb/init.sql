


-- Create the Config table
CREATE TABLE Config (
    id SERIAL PRIMARY KEY,
    name VARCHAR(120) UNIQUE NOT NULL,
    value VARCHAR(120) NOT NULL
);

-- Insert initial data into the Config table
INSERT INTO Config (name, value) VALUES
    ('howMuchTimeToFutrolajki', '621'),
    ('date', '6.2.1'),
    ('discord', 'abc'),
    ('website', 'https://futrolajki.pl/');
