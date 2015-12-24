/* Create DB */

DROP DATABASE IF EXISTS tournament;
CREATE DATABASE tournament;
\c tournament;

-- The players table containing a player's name and a unique id
CREATE TABLE players (
    name text NOT NULL,
    id serial PRIMARY KEY
);

-- The matches table contains records of each match and the winner and the
-- loser of each match
CREATE TABLE matches (
    winner int REFERENCES players (id),
    loser int REFERENCES players (id),
    PRIMARY KEY (winner, loser)
);

-- To prevent rematch btw players
CREATE UNIQUE INDEX matches_uniq_idx ON matches
   (greatest(winner, loser), least(winner, loser));

/* Create Views */
-- The number of matches each player has played
CREATE VIEW v_numMatches AS
    SELECT id, COUNT(winner) AS matchesPlayed
    FROM players LEFT JOIN matches
    ON (winner = id OR loser = id)
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
/* A view to return a table of the players and their win records, sorted by
 * wins */
CREATE VIEW v_playerStandings AS
    SELECT players.id, players.name, v_numWins.wins,
           v_numMatches.matchesPlayed AS matches
    FROM players
    LEFT JOIN v_numWins ON
    (players.id = v_numWins.id)
    JOIN v_numMatches ON (players.id = v_numMatches.id)
    ORDER BY wins DESC;
