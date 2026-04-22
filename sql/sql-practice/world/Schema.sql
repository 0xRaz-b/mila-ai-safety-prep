Schema · SQL
Copy

-- SQLZoo world table - schema
 
CREATE TABLE IF NOT EXISTS world (
    name        VARCHAR(100)    NOT NULL PRIMARY KEY,
    continent   VARCHAR(50)     NOT NULL,
    area        BIGINT,
    population  BIGINT,
    gdp         BIGINT,
    capital     VARCHAR(100),
    tld         VARCHAR(10)
);