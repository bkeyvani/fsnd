#!/usr/bin/env python

import random
import psycopg2
from tournament import connect, \
                       playerStandings, \
                       registerPlayer, \
                       reportMatch

def create_db():
    """
    Create tournament database.
    """
    # in order to create the tournament db we need to connect to postgres db
    # first and then execute db creation command.
    conn = psycopg2.connect(dbname='postgres')

    # autocommit needs to be set to ON in order to create or drop databases
    conn.set_session(autocommit=True)
    c = conn.cursor()
    c.execute("DROP DATABASE IF EXISTS tournament;")
    c.execute("CREATE DATABASE tournament;")

    # since autocommit is ON there is no need to commit
    c.close()
    conn.close()


def create_tables():
    """
    Create players and matches tables.
    """
    conn = connect()
    c = conn.cursor()

    # Create players table
    c.execute(
        """
        CREATE TABLE players (
            name text NOT NULL,
            id serial PRIMARY KEY
        );
        """)

    # Create matches table
    c.execute(
        """
        CREATE TABLE matches (
            p1 int REFERENCES players (id),
            p2 int REFERENCES players (id),
            winner int REFERENCES players (id)
        );
        """)
    conn.commit()
    conn.close()

def create_views():
    """
    Create the views for the following:

    v_numMatches: The number of matches each player has played
    v_numWins: The number of wins for each player
    v_playerStandings
    v_swissParings
    """
    conn = connect()
    c = conn.cursor()

    # Create v_numMatches view
    c.execute(
        """
        CREATE VIEW v_numMatches AS
            SELECT id, COUNT(winner) AS matchesPlayed
            FROM players LEFT JOIN matches
            ON (p1 = id OR p2 = id)
            GROUP BY players.id
            ORDER BY players.id;
        """)

    # Create v_numWins view
    c.execute(
        """
        CREATE VIEW v_numWins AS
            SELECT players.id, COUNT(winner) AS wins
            FROM players LEFT JOIN matches
            ON players.id = matches.winner
            GROUP BY players.id
            ORDER BY wins DESC;
        """)

    # Create v_playerStandings view
    c.execute(
        """
        CREATE VIEW v_playerStandings AS
            SELECT players.id, players.name, v_numWins.wins,
                   v_numMatches.matchesPlayed AS matches
            FROM players
            LEFT JOIN v_numWins ON
            (players.id = v_numWins.id)
            JOIN v_numMatches ON (players.id = v_numMatches.id)
            ORDER BY wins DESC;
        """)

    # Create v_swissParings view
    c.execute(
        """
        CREATE VIEW v_swissParings AS
            SELECT
                vps1.id AS id1,
                vps1.name AS name1,
                vps2.id AS id2,
                vps2.name AS name2
            FROM v_playerstandings vps1
            JOIN v_playerstandings vps2
            ON (vps1.wins = vps2.wins)
            AND vps1.id > vps2.id
            ORDER BY
                id1 DESC,
                id2 DESC;
        """)

    conn.commit()
    conn.close()


def match_players(groups, num_wins):
    """
    Randomly match players of each group together. Each group of players
    consitst of players in the same ranking (i.e. same number of wins)
    """
    for i in xrange(len(groups[num_wins]) / 2):
        winner_row = random.choice(groups[num_wins])
        winner_id = winner_row[0]
        groups[num_wins].remove(winner_row)
        loser_row = random.choice(groups[num_wins])
        loser_id = loser_row[0]
        groups[num_wins].remove(loser_row)
        reportMatch(winner_id, loser_id)


if __name__ == '__main__':
    # create the tournament DB
    create_db()

    # create tables and views
    create_tables()
    create_views()

    # Register players
    PLAYERS = ['Player 1', 'Player 2', 'Player 3', 'Player 4', 'Player 5', 'Player 6', 'Player 7', 'Player 8', 'Player 9', 'Player 10', 'Player 11', 'Player 12', 'Player 13', 'Player 14', 'Player 15', 'Player 16',]

    # Register all players
    for player in PLAYERS:
        registerPlayer(player)

    # Append initial player standings
    for game_round in xrange(4):
        ps = playerStandings()
        groups = []
        for num_wins in xrange(game_round + 1):
            groups.append([row for row in ps if row[2] == num_wins])
            match_players(groups, num_wins)
