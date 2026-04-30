-- ============================================================
-- SQLZoo Practice Solutions
-- Author: [Razine Bouache]
-- Tables used: world (name, continent, area, population, gdp)
-- =================

-- Q1 : Total world population
-- Show the total population of the world.

SELECT SUM(population)
FROM world

-- Q2 : List of continents
-- List all the continents - just once each


SELECT DISTINCT continent
FROM world 

-- Q3 : GDP of Africa
-- Give the total GDP of Africa

SELECT SUM(gdp)
FROM world
where continent = 'africa'

-- Q4: Count the big countries
-- How many countries have an area of at least 1000000

SELECT COUNT(name)
FROM world
where area >= 1000000

-- Q5: Baltic states population
-- What is the total population of ('Estonia', 'Latvia', 'Lithuania')

SELECT SUM(population)
FROM world 
where name IN ('Estonia', 'Latvia', 'Lithuania')

-- Q6: Using GROUP BY and HAVING
-- For each continent show the continent and number of countries.

SELECT continent, COUNT(name)
FROM world
GROUP BY continent

-- Q7: Counting big countries in each continent
-- For each continent show the continent and number of countries with populations of at least 10 million.

SELECT continent, COUNT(name)
FROM world
WHERE population > 10000000
GROUP BY continent
