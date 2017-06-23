-- Table definitions for the tournament project.

DROP DATABASE IF EXISTS tournament;
CREATE DATABASE tournament;
\c tournament;

CREATE TABLE Player (
	name text, 
	id serial primary key
	);

CREATE TABLE Matches(
	match_id serial primary key,
	winner_id integer references Player(id),
	loser_id integer references Player(id)
	);

CREATE VIEW winners as 
	SELECT winner_id, count(*) as wins 
	FROM Matches
	GROUP BY winner_id;

CREATE VIEW losers as
	SELECT loser_id, count(*) as losses
	FROM Matches
	GROUP BY loser_id;

CREATE VIEW ranking as 
	SELECT id, name, coalesce(wins,0) as wins, (coalesce(wins,0) + coalesce(losses,0)) as matches 
	FROM Player LEFT JOIN winners ON  (id = winner_id)
				LEFT JOIN losers  ON  (id = loser_id)
	ORDER BY wins desc;
