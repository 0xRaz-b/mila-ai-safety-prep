-- Drop existing table if exists
DROP TABLE IF EXISTS employee;

-- Table creation
CREATE TABLE employee (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    departement VARCHAR(50),
    salary INTEGER
);

-- Sample data
INSERT INTO employee (name, departement, salary) VALUES ('Alice', 'Data', 75000);
INSERT INTO employee (name, departement, salary) VALUES ('Bob', 'Dev', 80000);
INSERT INTO employee (name, departement, salary) VALUES ('Carla', 'Data', 72000);
INSERT INTO employee (name, departement, salary) VALUES ('David', 'Dev', 85000);