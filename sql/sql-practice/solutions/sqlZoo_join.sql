-- ============================================================
-- SQLZoo Practice Solutions
-- Author: [Razine Bouache]
-- Tables used:
-- game    (id, mdate, stadium, team1, team2)
-- goal    (matchid, teamid, player, gtime)
-- eteam   (id, teamname, coach)
-- =================


-- Q1: Bender
-- The first example shows the goal scored by a player with the last name 'Bender'. The * says to list all the columns in the table - a shorter way of saying matchid, teamid, player, gtime
-- Modify it to show the matchid and player name for all goals scored by Germany. To identify German players, check for: teamid = 'GER'

SELECT matchid, player
FROM goal
WHERE teamid = 'GER'

-- Q2: Teams
-- From the previous query you can see that Lars Bender's scored a goal in game 1012. Now we want to know what teams were playing in that match.
-- Notice in the that the column matchid in the goal table corresponds to the id column in the game table. We can look up information about game 1012 by finding that row in the game table.
-- Show id, stadium, team1, team2 for just game 1012

SELECT id,stadium,team1,team2
FROM game
WHERE id = 1012


-- Q3: A JOIN
-- Show the player, teamid, stadium and mdate for every German goal.


SELECT player, teamid, stadium, mdate
FROM game JOIN goal ON (id = matchid)
WHERE teamid = 'GER'

-- Q4: Mario
-- Show the team1, team2 and player for every goal scored by a player called Mario player LIKE 'Mario%'

SELECT team1, team2, player
FROM game JOIN goal ON (game.id = goal.matchid)
WHERE player LIKE 'Mario%'


-- Q5: Team Coach
-- Show player, teamid, coach, gtime for all goals scored in the first 10 minutes gtime<=10

SELECT player, teamid,coach,gtime
FROM goal JOIN eteam on (goal.teamid = eteam.id)
WHERE gtime<=10

-- Q6: Disambiguation
-- List the dates of the matches and the name of the team in which 'Fernando Santos' was the team1 coach.

SELECT mdate, teamname
FROM game JOIN eteam ON (game.team1 = eteam.id)
where coach = 'Fernando Santos'

-- Q7: Stadiums
-- List the player for every goal scored in a game where the stadium was 'National Stadium, Warsaw'

SELECT player 
FROM game JOIN goal ON (game.id = goal.matchid)
where stadium LIKE 'National Stadium, Warsaw'

-- Q8: Scoring against Germany
-- Show the name of all players who scored a goal against Germany.

SELECT DISTINCT player
FROM game JOIN goal ON matchid = id
WHERE (team1='GER' OR team2='GER') AND teamid != 'GER'

-- Q9: Total goals scored
-- Show teamname and the total number of goals scored.

SELECT teamname, COUNT(*) 
FROM eteam JOIN goal ON (eteam.id = goal.teamid)
GROUP BY teamname

-- Q10: Stadium and goal total
-- Show the stadium and the number of goals scored in each stadium.

SELECT stadium, COUNT(*)
FROM game JOIN goal on (goal.matchid = game.id)
GROUP BY stadium

-- Q11: Polish goals
-- For every match involving 'POL', show the matchid, date and the number of goals scored.

SELECT matchid,mdate, COUNT(*)
FROM game JOIN goal ON (matchid = id)
WHERE (team1 = 'POL' OR team2 = 'POL')
GROUP BY matchid,mdate

-- Q12: German matches
-- For every match where 'GER' scored, show matchid, match date and the number of goals scored by 'GER'

SELECT matchid, mdate, COUNT(*)
FROM game JOIN goal ON ( game.id = goal.matchid)
WHERE teamid ='GER'
GROUP BY matchid,mdate