-- Create the simple_command table
CREATE TABLE simple_command (
    id SERIAL PRIMARY KEY,
    name VARCHAR(120) UNIQUE NOT NULL,
    value VARCHAR(120) NOT NULL,
    description VARCHAR(120) NOT NULL
);

-- Insert initial data into the simple_command table
INSERT INTO simple_command (name, value, description) VALUES
    ('date', '13–17.11.2024', 'Data futrołajek'),
    ('website', 'https://futrolajki.pl/', 'Strona konwentu'),
    ('program', 'https://futrolajki.pl/', 'Program konwentu');

-- Create the config table
CREATE TABLE config (
    id SERIAL PRIMARY KEY,
    name VARCHAR(120) UNIQUE NOT NULL,
    value VARCHAR(120) NOT NULL,
    description VARCHAR(120) NOT NULL
);

-- Insert initial data into the config table
INSERT INTO config (name, value, description) VALUES
    ('photo_upload', '0', '0 lub 1 w zależności czy komenda /zdjęcia do uploadowania zdjęć ma być aktywna');

-- Create the verified_users table
CREATE TABLE verified_users (
    id INTEGER PRIMARY KEY, -- ID telegram
    username VARCHAR(120) UNIQUE NOT NULL, -- nick foxcons
    id_username INTEGER UNIQUE NOT NULL, -- ID foxcons
    is_verified BOOLEAN NOT NULL, -- czy zweryfikowany
    room BOOLEAN NOT NULL, -- czy ma pokój
    plan_id INTEGER NOT NULL, -- plan
    plan_selected VARCHAR(30) NOT NULL, -- jaki wybrany plan
    plan_paid BOOLEAN NOT NULL -- czy zapłacony
);

-- Insert initial data into the verified_users table
INSERT INTO verified_users (id, username, id_username, is_verified, room, plan_id, plan_selected, plan_paid) VALUES
    (123456789, 'nick', 123456789, TRUE, TRUE, 1, 'plan1', TRUE),
    (987654321, 'nick2', 987654321, TRUE, TRUE, 2, 'plan2', TRUE);
