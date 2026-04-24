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


-- Q5: Literature in the 1980's
-- Show all details (yr, subject, winner) of the literature prize winners for 1980 to 1989 inclusive.

SELECT yr,subject,winner
FROM nobel 
WHERE yr >=1980
AND yr <= 1989
AND subject = 'literature'

-- Q6 Only Presidents
-- Show all details of the presidential winners:

SELECT * FROM nobel
 WHERE winner IN ('Theodore Roosevelt',
                  'Thomas Woodrow Wilson',
                  'Jimmy Carter','Barack Obama')

-- Q7 John
-- Show the winners with first name John

SELECT winner 
FROM nobel 
WHERE winner LIKE 'John%'

-- Q8 Chemistry and Physics from different years
-- Show the year, subject, and name of physics winners for 1980 together with the chemistry winners for 1984.

SELECT * 
FROM nobel 
WHERE (yr = 1980 AND subject = 'physics')
OR (yr = 1984 AND subject = 'chemistry')

-- Q9 Exclude Chemists and Medics
-- Show the year, subject, and name of winners for 1980 excluding chemistry and medicine

SELECT * 
FROM nobel 
WHERE yr = 1980 
AND subject <> 'chemistry'
AND subject <> 'medicine' 

-- Q10 Early Medicine, Late Literature
-- Show year, subject, and name of people who won a 'Medicine' prize in an early year (before 1910, not including 1910) together with winners of a 'Literature' prize in a later year (after 2004, including 2004)

SELECT * 
FROM nobel
WHERE (subject ='Medicine'
AND yr < 1910)
OR (subject = 'Literature' and yr >= 2004)

-- Q11 Umlaut
-- Find all details of the prize won by PETER GRÜNBERG

SELECT *
FROM nobel
WHERE winner = 'PETER GRÜNBERG' 

-- Q12 Apostrophe
-- Find all details of the prize won by EUGENE O'NEILL

SELECT * 
FROM nobel 
WHERE winner = CONCAT ('EUGENE O','NEILL')