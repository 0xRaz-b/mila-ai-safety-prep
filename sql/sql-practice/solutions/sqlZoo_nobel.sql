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

-- Q2: 1962 Literature
-- Find the price of literature for a certain year 

SELECT winner
FROM nobel
WHERE yr = 1962
AND subject = 'literature'

-- Q3: Albert Einstein
-- Find when Sir Einstein won the nobel price and the concerned topic 

SELECT yr, subject
FROM nobel
WHERE winner = 'Albert Einstein'

-- Q4: Recent Peace Prizes
-- Find winner of peace prize since 2000

SELECT winner
FROM nobel 
WHERE subject = 'Peace'
AND yr >= 2000

