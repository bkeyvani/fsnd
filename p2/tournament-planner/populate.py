#!/usr/bin/env python

import math
import psycopg2
import random
import sys
from tournament import connect, \
                       playerStandings, \
                       registerPlayer, \
                       reportMatch, \
                       swissPairings
from util.logger import logger

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
            winner int REFERENCES players (id),
            loser int REFERENCES players (id),
            PRIMARY KEY (winner, loser)
        );
        """)
    conn.commit()
    conn.close()

def create_indices():
    """
    Create indices for tables.
    """
    conn = connect()
    c = conn.cursor()

    # To prevent rematch btw players
    c.execute(
        """
        CREATE UNIQUE INDEX matches_uniq_idx ON matches
           (greatest(winner, loser), least(winner, loser));
        """)
    conn.commit()
    conn.close()

def create_views():
    """
    Create the views for the following:

    v_numMatches: The number of matches each player has played
    v_numWins: The number of wins for each player
    v_playerStandings
    """
    conn = connect()
    c = conn.cursor()

    # Create v_numMatches view
    c.execute(
        """
        CREATE VIEW v_numMatches AS
            SELECT id, COUNT(winner) AS matchesPlayed
            FROM players LEFT JOIN matches
            ON (winner = id OR loser = id)
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

    conn.commit()
    conn.close()


if __name__ == '__main__':
    # start logging
    logger.info('Started')

    # create the tournament DB
    create_db()
    logger.info('Created DB')

    # create tables and views
    create_tables()
    logger.info('Created tables')
    create_indices()
    logger.info('Created indices')
    create_views()
    logger.info('Created views')

    # Register players
    PLAYERS = ['Player 1', 'Player 2', 'Player 3', 'Player 4', 'Player 5', 'Player 6', 'Player 7', 'Player 8', 'Player 9', 'Player 10', 'Player 11', 'Player 12', 'Player 13', 'Player 14', 'Player 15', 'Player 16', 'Player 17', 'Player 18', 'Player 19', 'Player 20', 'Player 21', 'Player 22', 'Player 23', 'Player 24', 'Player 25', 'Player 26', 'Player 27', 'Player 28', 'Player 29', 'Player 30', 'Player 31', 'Player 32', 'Player 33', 'Player 34', 'Player 35', 'Player 36', 'Player 37', 'Player 38', 'Player 39', 'Player 40', 'Player 41', 'Player 42', 'Player 43', 'Player 44', 'Player 45', 'Player 46', 'Player 47', 'Player 48', 'Player 49', 'Player 50', 'Player 51', 'Player 52', 'Player 53', 'Player 54', 'Player 55', 'Player 56', 'Player 57', 'Player 58', 'Player 59', 'Player 60', 'Player 61', 'Player 62', 'Player 63', 'Player 64',]

    # Shuffle PLAYERS in order to have a random list
    random.shuffle(PLAYERS)

    # Register all players
    for player in PLAYERS:
        registerPlayer(player)

    logger.info('Registered all players')
    game_rounds = int(math.log(len(PLAYERS), 2))

    # Allow the app to try 5 times before gracefully quiting with an error
    # message.
    tries = 1
    for game_round in xrange(game_rounds):
        logger.info('%s Round: %s %s', '=' * 10, game_round, '=' * 10)
        try:
            logger.info("\t'populate.py' Try: %s", tries)
            sp = swissPairings()
            for pair in sp:
                winner_id = pair[0]
                loser_id = pair[2]
                reportMatch(winner_id, loser_id)
        except psycopg2.IntegrityError as e:
            logger.error(e)
            tries += 1

        if tries > 5:
            msg = """
            The app exceeded number of allowed tries (5). Please try again
            later.
            """
            logger.info(msg)
            print msg
            sys.exit(1)

    msg = "All players matched successfully in %s attempts!" % tries
    logger.info(msg)
    print msg
    sys.exit(0)
