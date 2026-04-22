-- ============================================================
-- SQLZoo Practice Solutions
-- Author: [Your name]
-- Tables used: world (name, continent, area, population, gdp)
--              nobel (yr, subject, winner)
-- ============================================================


-- ============================================================
-- SECTION 1: SELECT Basics
-- ============================================================

-- Q1: Introduction
-- Get the population of Germany
SELECT population FROM world
WHERE name = 'Germany';

-- Q2: Scandinavia
-- Get the name and population of Sweden, Norway and Denmark
SELECT name, population FROM world
WHERE name IN ('Sweden', 'Norway', 'Denmark');

-- Q3: Just the right size
-- Get countries with an area between 200,000 and 250,000 sq km
SELECT name, area FROM world
WHERE area BETWEEN 200000 AND 250000;


-- ============================================================
-- SECTION 2: SELECT From World
-- ============================================================

-- Q1: Introduction
-- Get the name, continent and population of all countries
SELECT name, continent, population FROM world;

-- Q2: Large Countries
-- Get countries with a population of at least 200 million
SELECT name FROM world
WHERE population > 200000000;

-- Q3: Per Capita GDP
-- Get the per capita GDP of countries with a population of at least 200 million
SELECT name, gdp/population FROM world
WHERE population > 200000000;

-- Q4: South America In Millions
-- Get the population in millions for countries in South America
SELECT name, population/1000000 FROM world
WHERE continent = 'South America';

-- Q5: France, Germany, Italy
-- Get the name and population of France, Germany and Italy
SELECT name, population FROM world
WHERE name IN ('France', 'Germany', 'Italy');

-- Q6: United
-- Get countries whose name contains the word 'United'
SELECT name FROM world
WHERE name LIKE '%United%';

-- Q7: Two Ways to Be Big
-- Get countries that are large by area (> 3M km²) or by population (> 250M)
SELECT name, population, area FROM world
WHERE area > 3000000 OR population > 250000000;

-- Q8: One or the Other (but not both)
-- Get countries that are large by area or population, but not both
SELECT name, population, area FROM world
WHERE area > 3000000 XOR population > 250000000;

-- Q9: Rounding - South America
-- Get population (in millions) and GDP (in billions) for South American countries, rounded to 2 decimal places
SELECT name, ROUND(population/1000000, 2), ROUND(gdp/1000000000, 2)
FROM world
WHERE continent = 'South America';

-- Q10: Trillion Dollar Economies
-- Get the per capita GDP (rounded to the nearest 1000) for countries with a GDP over 1 trillion
SELECT name, ROUND(gdp/population, -3)
FROM world
WHERE gdp > 1000000000000;