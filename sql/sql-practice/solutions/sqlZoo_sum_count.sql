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