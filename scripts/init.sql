\c postgres;

-- Create a simple table within the "postgres" database
CREATE TABLE IF NOT EXISTS userDetails (
            name VARCHAR(50) PRIMARY KEY,
            password VARCHAR(50)
);

INSERT INTO userDetails (name ,password) VALUES ('thomas','password') ON CONFLICT DO NOTHING
INSERT INTO userDetails (name ,password) VALUES ('avishek','password') ON CONFLICT DO NOTHING

