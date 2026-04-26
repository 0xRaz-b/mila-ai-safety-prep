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