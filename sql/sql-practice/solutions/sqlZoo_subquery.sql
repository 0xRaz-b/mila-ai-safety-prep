-- ============================================================
-- SQLZoo Practice Solutions
-- Author: [Razine Bouache]
-- Tables used: world (name, continent, area, population, gdp)
-- ============================================================


-- Q1: Bigger than Russia
-- List each country name where the population is larger than that of 'Russia'.

SELECT name FROM world
  WHERE population >
     (SELECT population FROM world
      WHERE name='Russia')

-- Q2: Richer than UK
-- Show the countries in Europe with a per capita GDP greater than 'United Kingdom'.

SELECT name
FROM world
WHERE continent = 'Europe' 
AND gdp/population > ( SELECT gdp/population FROM world WHERE name = 'United Kingdom')

-- Q3: Neighbours of Argentina and Australia
-- List the name and continent of countries in the continents containing either Argentina or Australia. Order by name of the country.

SELECT name, continent 
FROM world
WHERE continent IN 
(SELECT continent FROM world 
WHERE name IN ('Australia','Argentina'))
ORDER BY name 

-- Q4 Between Canada and Poland
-- Which country has a population that is more than United Kingdom but less than Germany? Show the name and the population.

SELECT name, population 
FROM world 
WHERE population > 
(SELECT  population 
FROM world
WHERE name = 'United Kingdom') AND 
population < (SELECT  population 
FROM world
WHERE name = 'Germany') 

-- Q5 Percentages of Germany
-- Show the name and the population of each country in Europe. Show the population as a percentage of the population of Germany.

SELECT name, CONCAT(ROUND (population / (SELECT population from world WHERE name = 'Germany') *100,0), '%')
FROM world
WHERE continent = 'Europe'