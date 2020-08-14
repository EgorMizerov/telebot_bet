import sqlite3 as lite
import sys

con = lite.connect('bot.db')

with con:
    cur = con.cursor()
    cur.execute("SELECT * FROM payment_query WH")
    rows = cur.fetchall()
    print(type(rows))
    print(rows)

    for row in rows:
        print(row)