-- ============================================================
-- SQLZoo Practice Solutions
-- Author: [Razine Bouache]
-- Tables used: nobel (yr, subject, winner)
-- Link to the tab : https://sqlzoo.net/wiki/SELECT_from_Nobel_Tutorial          
-- ============================================================

-- Q1: Winners from 1950
-- Get the all nobel prices for that year 

SELECT yr, subject, winner
FROM nobel
WHERE yr = 1950

-- Q1: 1962 Literature
-- Find the price of literature for a certain year 

SELECT winner
FROM nobel
WHERE yr = 1962
AND subject = 'literature'
