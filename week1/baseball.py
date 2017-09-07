##  This is the Exercise1 for Introduction to Data Science course
##  Get the database from here and extract it: https://www.kaggle.com/seanlahman/the-history-of-baseball
##  Univ. of Helsinki, Ege Can Ozer - 014692310

import sqlite3
import pandas as pd

database = 'data/baseball.sqlite'
conn = sqlite3.connect(database)

query = "SELECT count(*) as count_of_inducted_Y_players" \
        " FROM player as p" \
        " INNER JOIN hall_of_fame as hof" \
        " ON hof.player_id = p.player_id" \
        " WHERE hof.inducted = 'Y'"

res = pd.read_sql(query, conn)
print(res)

# Check the result is correct
assert res.count_of_inducted_Y_players[0] == 312,\
    "Incorrect count %r" % res.count_of_inducted_Y_players[0]


query = "SELECT main.college_id as college, count(*) as player_count" \
        " FROM" \
            " (SELECT p.player_id, pc.college_id, pc.year" \
            " FROM player as p" \
            " INNER JOIN hall_of_fame as hof " \
            "ON hof.player_id = p.player_id " \
            "INNER JOIN player_college as pc " \
            "ON pc.player_id = p.player_id " \
            "WHERE hof.inducted = 'Y' " \
            "GROUP BY pc.player_id " \
            "ORDER BY pc.college_id) as main " \
        "GROUP BY main.college_id " \
        "ORDER BY player_count DESC"


res = pd.read_sql(query, conn)
print(res[0:5])

conn.close()

