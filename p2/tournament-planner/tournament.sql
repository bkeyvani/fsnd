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

/* Populate DB */
-- Players
INSERT INTO players VALUES ('Player 1');
INSERT INTO players VALUES ('Player 2');
INSERT INTO players VALUES ('Player 3');
INSERT INTO players VALUES ('Player 4');
INSERT INTO players VALUES ('Player 5');
INSERT INTO players VALUES ('Player 6');
INSERT INTO players VALUES ('Player 7');
INSERT INTO players VALUES ('Player 8');
INSERT INTO players VALUES ('Player 9');
INSERT INTO players VALUES ('Player 10');
INSERT INTO players VALUES ('Player 11');
INSERT INTO players VALUES ('Player 12');
INSERT INTO players VALUES ('Player 13');
INSERT INTO players VALUES ('Player 14');
INSERT INTO players VALUES ('Player 15');
INSERT INTO players VALUES ('Player 16');

-- Sample matches
-- Round 1
INSERT INTO matches VALUES (1, 2, 2);
INSERT INTO matches VALUES (3, 4, 4);
INSERT INTO matches VALUES (5, 6, 6);
INSERT INTO matches VALUES (7, 8, 8);
INSERT INTO matches VALUES (9, 10, 10);
INSERT INTO matches VALUES (11, 12, 12);
INSERT INTO matches VALUES (13, 14, 14);
INSERT INTO matches VALUES (15, 16, 16);

-- Round 2
INSERT INTO matches VALUES (2, 4, 4);
INSERT INTO matches VALUES (6, 8, 8);
INSERT INTO matches VALUES (10, 12, 12);
INSERT INTO matches VALUES (14, 16, 16);
INSERT INTO matches VALUES (1, 3, 3);
INSERT INTO matches VALUES (5, 7, 7);
INSERT INTO matches VALUES (9, 11, 11);
INSERT INTO matches VALUES (13, 15, 15);

-- Round 3
INSERT INTO matches VALUES (4, 8, 8);
INSERT INTO matches VALUES (12, 16, 16);
INSERT INTO matches VALUES (2, 6, 6);
INSERT INTO matches VALUES (10, 14, 14);
INSERT INTO matches VALUES (3, 7, 7);
INSERT INTO matches VALUES (11, 15, 15);
INSERT INTO matches VALUES (1, 5, 5);
INSERT INTO matches VALUES (9, 13, 13);

-- Round 4
INSERT INTO matches VALUES (8, 16, 16);
INSERT INTO matches VALUES (4, 12, 12);
INSERT INTO matches VALUES (6, 14, 14);
INSERT INTO matches VALUES (7, 15, 15);
INSERT INTO matches VALUES (2, 10, 10);
INSERT INTO matches VALUES (3, 11, 11);
INSERT INTO matches VALUES (5, 13, 13);
INSERT INTO matches VALUES (1, 9, 9);
