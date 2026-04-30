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

