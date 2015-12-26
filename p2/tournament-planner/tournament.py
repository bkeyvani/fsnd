#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
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
    c.execute("SELECT * FROM matches ORDER BY winner DESC;")
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
    # a list of all previous matches
    prev_matches = getMatches()

    pairs = []
    while len(ps):
        # grab the first player from the player standings list
        p1 = ps.pop(0)
        p1_id = p1[0]
        p1_name = p1[1]
        p1_wins = p1[2]
        # get a list of all players with the same wins or one less
        same_rank = [row for row in ps if row[2] == p1_wins]
        # reverse same_rank to reduce the chance of trying to pair already
        # matched players
        same_rank.reverse()
        # pair the next player from the same_rank list who has not been
        # matched before.
        for p2 in same_rank:
            p2_id = p2[0]
            p2_name = p2[1]
            if p1_id != p2_id and not(
                (p1_id, p2_id) in prev_matches or
                (p2_id, p1_id) in prev_matches):
                pairs.append((p1_id, p1_name, p2_id, p2_name))
                ps.remove(p2)
                break
            else:
                logger.warn('skipped: %s', (p1_id, p2_id))

    return pairs
