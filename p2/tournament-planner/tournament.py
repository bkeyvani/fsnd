#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
import random
import time
from util.logger import logger


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    conn = connect()
    c = conn.cursor()
    c.execute("DELETE FROM matches;")
    conn.commit()
    conn.close()


def deletePlayers():
    """Remove all the player records from the database."""
    conn = connect()
    c = conn.cursor()
    c.execute("DELETE FROM players;")
    conn.commit()
    conn.close()


def countPlayers():
    """Returns the number of players currently registered."""
    conn = connect()
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM players;")
    result = c.fetchone()
    conn.commit()
    conn.close()
    count = result[0]
    return count


def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    conn = connect()
    c = conn.cursor()
    c.execute("INSERT INTO players VALUES (%s);", (name,))
    conn.commit()
    conn.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    conn = connect()
    c = conn.cursor()
    c.execute("SELECT * FROM v_playerStandings;")
    results = c.fetchall()
    conn.commit()
    conn.close()
    return results


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    conn = connect()
    c = conn.cursor()
    c.execute(
        "INSERT INTO matches VALUES (%s, %s);",
        (winner, loser))
    conn.commit()
    conn.close()


def getMatches():
    """Returns a list of previous matches between players, sorted by winner.

    This list is used to lookup previous matches and avoid rematches between
    players.

    Returns:
      A list of tuples, each of which contains (winner, loser):
        winner: the winner's id (assigned by the database)
        loser: the loser's id (assigned by the database)
    """
    conn = connect()
    c = conn.cursor()
    c.execute( "SELECT * FROM matches ORDER BY winner DESC;")
    results = c.fetchall()
    conn.commit
    conn.close()
    return results

def swissPairings():
    """Returns a list of pairs of players for the next round of a match.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    # ps is a list of (id, name, wins, matches) tuples
    ps = playerStandings()

    # get all previous matches
    matches = getMatches()

    # pairs is a list of randomly mached players with the same rank that
    # weren't matched before
    # e.g.
    #     [((id1, name1, wins1, matches1), (id2, name2, wins2, matches2)),
    #      ((id3, name3, wins3, matches3), (id4, name4, wins4, matches4)),
    #      ...]
    pairs = []

    # max number of wins in playerStandings
    max_wins = ps[0][2]

    # group players by ranks
    groups = {}
    for num_wins in xrange(max_wins + 1):
        same_rank = [row for row in ps if row[2] == num_wins]
        groups[num_wins] = same_rank

    # seed the random function with time.time() to ensure unique and different
    # seeds each time this function runs.
    random.seed(time.time())

    # randomly match potential players in each group
    for i in xrange(max_wins + 1):
        tries = 1
        msg = "Randomly matching players with %s wins." % i
        logger.info(msg)
        while len(groups[i]):
            logger.info("\t'swissPairings' Try: %s", tries)
            winner = random.choice(groups[i])
            winner_id = winner[0]
            winner_name = winner[1]
            loser = random.choice(groups[i])
            loser_id = loser[0]
            loser_name = loser[1]

            # If players are not the same and were not previously matched, add
            # them to pairs
            if winner != loser and not (
                    (winner_id, loser_id) in matches or
                    (loser_id, winner_id) in matches
                ):
                pairs.append((winner_id, winner_name, loser_id, loser_name))
                # remove matched players from list
                groups[i].remove(winner)
                groups[i].remove(loser)
            else:
                tries += 1
            if tries > 5:
                msg = "Exceeded number of tries (5) on (%s, %s)" % (
                    winner_id, loser_id)
                raise RuntimeError(msg)

    return pairs
