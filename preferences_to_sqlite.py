import sqlite3
import hashlib
from datetime import datetime

try:
    conn = sqlite3.connect("festivals.db") or die ("Impossible to connect to/create database file")
    cur = conn.cursor()

    cur_year = datetime.now().year
    # we're planning for next year at this point
    if datetime.now().month >= 9:
        cur_year += 1

    try:
        params = (cur_year,)
        res = cur.execute("SELECT year FROM years WHERE year = ?", params)
        if res.fetchone() is None:
            print("Adding to year table" + str(cur_year))
            cur.execute ("INSERT INTO years (year) VALUES (?)", params)
            conn.commit()
    except Exception as e:
        print(e)
        print("Unable to manage years table")

    try:
        pres = open('preferences.csv', 'r')

        i = 0
        user_ids = []
        for band in pres:
            if i == 0:
                user_list = band.split(';')
                for user in user_list:
                    user = user.strip()

                    if user != "":
                        # this will be used later for inserting artist presences
                        user_ids.append(hashlib.sha1((user).encode('utf-8')).hexdigest())
                        try:
                            params = {"id" : hashlib.sha1(user.encode('utf-8')).hexdigest(), "name" : user }
                            res = cur.execute("SELECT name FROM users WHERE name = :name", params)
                            if res.fetchone() is None:
                                print("Adding to user table: " + user)
                                cur.execute("INSERT INTO users (id, name) VALUES (:id, :name)", params)
                                conn.commit()
                        except Exception as e:
                            print(e)
                            print("Unable to manage users table")

            band_name = (band.split(';'))[0]
            band_name = band_name.strip()
            if (band_name != ""):
                try:
                    params = {"id" : hashlib.sha1(band_name.encode('utf-8')).hexdigest(), "name" : band_name }
                    res = cur.execute("SELECT name FROM artist WHERE name = :name", params)
                    if res.fetchone() is None:
                        print("Adding to artist table: " + band_name)
                        cur.execute("INSERT INTO artist (id, name) VALUES (:id, :name)", params)
                        conn.commit()
                except Exception as e:
                    print(e)
                    print("Unable to manage artist table")

                j = 0
                for vote in band.split(';'):
                    if j == 0:
                        j += 1
                        continue
                    if vote == "":
                        vote = "0"
                    if j >= len(user_ids) - 1:
                        break
                    try:
                        params = {"id_artist" : hashlib.sha1(band_name.encode('utf-8')).hexdigest(), "id_user" : user_ids[j - 1], "year" : cur_year, "vote" : vote }
                        res = cur.execute("SELECT vote FROM preferences WHERE id_artist = :id_artist AND id_user = :id_user AND id_year = :year", params)
                        found = res.fetchone()
                        if found is None:
                            print("Inserting user preference for: " + band_name + ", vote: " + vote)
                            cur.execute("INSERT INTO preferences (id_user, id_year, id_artist, vote) VALUES (:id_user, :year, :id_artist, :vote)", params)
                            conn.commit()
                        else:
                            if vote != found[0]:
                                print("Updating user preference for: " + band_name + ", column " + str(j) + " to vote: " + vote)
                                cur.execute("UPDATE preferences SET vote = :vote WHERE id_user = :id_user AND id_year = :year AND id_artist = :id_artist", params)
                                conn.commit()

                    except Exception as e:
                        print(e)
                        print("Unable to manage presences table")
                    j += 1

            i += 1

    except IOError:
        exit('file not found')

    conn.close()
except Exception as e:
    print(e)
    exit('Unable to open db')

