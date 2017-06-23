#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2

def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    conn = connect()
    c = conn.cursor()
    c.execute("DELETE FROM Matches;")
    conn.commit()
    conn.close()
    return


def deletePlayers():
    """Remove all the player records from the database."""
    conn=connect()
    c = conn.cursor()
    c.execute("DELETE FROM Player;")
    conn.commit()
    conn.close()
    return 0


def countPlayers():
    """Returns the number of players currently registered."""
    conn = connect()
    c = conn.cursor()
    c.execute("SELECT count (id) as num_players FROM Player;")
    result = c.fetchone()[0]
    conn.close()
    return result


def registerPlayer(name):
    """Adds a player to the tournament database.
    """
    conn = connect()
    c = conn.cursor()
    c.execute("INSERT INTO Player VALUES (%s)", (name,))
    conn.commit()
    conn.close()
    return


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
    c.execute("SELECT id, name, wins, matches FROM ranking ORDER BY wins DESC;")
    player_result = c.fetchall()
    conn.close()
    return player_result



def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    conn=connect()
    c = conn.cursor()
    c.execute("INSERT INTO Matches (match_id, winner_id, loser_id) VALUES (DEFAULT, %s, %s)", (winner, loser, ))
    conn.commit()
    conn.close()
    return
 
 
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
    i = 0
    pairings = []
    player_result = playerStandings()
    for i in range(0, len(player_result), 2):
        collect_players = player_result[i][0], player_result[i][1], player_result[i+1][0], player_result[i+1][1]
        pairings.append(collect_players)
    
    return pairings


