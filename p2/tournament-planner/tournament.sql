/* Create DB */

DROP DATABASE IF EXISTS tournament;
CREATE DATABASE tournament;
\c tournament;

CREATE TABLE players (
    name text NOT NULL,
    id serial PRIMARY KEY
);

CREATE TABLE matches (
    p1 int REFERENCES players (id),
    p2 int REFERENCES players (id),
    winner int REFERENCES players (id)
);

/* Create Views */
-- The number of matches each player has played
CREATE VIEW v_numMatches AS
    SELECT id, COUNT(*) AS matchesPlayed
    FROM players, matches
    WHERE p1 = id or p2 = id
    GROUP BY players.id
    ORDER BY players.id;

-- The number of wins for each player
CREATE VIEW v_numWins AS
    SELECT players.id, COUNT(winner) AS wins
    FROM players LEFT JOIN matches
    ON players.id = matches.winner
    GROUP BY players.id
    ORDER BY wins DESC;

-- The player standings
CREATE VIEW v_playerStandings AS
    SELECT players.id, players.name, v_numWins.wins,
           v_numMatches.matchesPlayed AS matches
    FROM players
    LEFT JOIN v_numWins ON
    (players.id = v_numWins.id)
    JOIN v_numMatches ON (players.id = v_numMatches.id)
    ORDER BY wins DESC;
