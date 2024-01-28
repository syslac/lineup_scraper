import sqlite3

conn = sqlite3.connect("festivals.db") or die ("Impossible to connect to/create database file")
cur = conn.cursor()

try:
    cur.execute("SELECT * FROM festival")
except sqlite3.OperationalError as e:
    try:
        cur.execute("CREATE TABLE festival(id, name, link, location, distance)")
    except Exception as e:
        print("Festival table already existing, but empty")

try:
    cur.execute("SELECT * FROM years")
except sqlite3.OperationalError as e:
    try:
        cur.execute("CREATE TABLE years(year)")
    except Exception as e:
        print("Years table already existing, but empty")

try:
    cur.execute("SELECT * FROM festival_edition")
except sqlite3.OperationalError as e:
    try:
        cur.execute("CREATE TABLE festival_edition(id, id_festival, id_year, date, ticket_price, travel_price)")
    except Exception as e:
        print("Festival edition table already existing, but empty")

try:
    cur.execute("SELECT * FROM artist")
except sqlite3.OperationalError as e:
    try:
        cur.execute("CREATE TABLE artist(id, name)")
    except Exception as e:
        print("Artist table already existing, but empty")

try:
    cur.execute("SELECT * FROM presences")
except sqlite3.OperationalError as e:
    try:
        cur.execute("CREATE TABLE presences(id_festival_edition, id_artist)")
    except Exception as e:
        print("Presences table already existing, but empty")

try:
    cur.execute("SELECT * FROM users")
except sqlite3.OperationalError as e:
    try:
        cur.execute("CREATE TABLE users(id, name)")
    except Exception as e:
        print("Users table already existing, but empty")

try:
    cur.execute("SELECT * FROM preferences")
except sqlite3.OperationalError as e:
    try:
        cur.execute("CREATE TABLE preferences(id_user, id_year, id_artist, vote)")
    except Exception as e:
        print("Preferences table already existing, but empty")

conn.close()
