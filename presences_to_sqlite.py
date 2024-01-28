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
        pres = open('presences.csv', 'r')

        i = 0
        festival_edition_ids = []
        for band in pres:
            if i == 0:
                festival_list = band.split(';')
                for festival in festival_list:
                    festival = festival.strip()

                    # this will be used later for inserting artist presences
                    festival_edition_ids.append(hashlib.sha1((festival+str(cur_year)).encode('utf-8')).hexdigest())
                    if festival != "":
                        try:
                            params = {"id" : hashlib.sha1(festival.encode('utf-8')).hexdigest(), "name" : festival }
                            res = cur.execute("SELECT name FROM festival WHERE name = :name", params)
                            if res.fetchone() is None:
                                print("Adding to festival table: " + festival)
                                cur.execute("INSERT INTO festival (id, name) VALUES (:id, :name)", params)
                                conn.commit()
                        except Exception as e:
                            print(e)
                            print("Unable to manage festival table")
                        try:
                            params = {"id_festival" : hashlib.sha1(festival.encode('utf-8')).hexdigest(), "id_year" : cur_year, "id": hashlib.sha1((festival+str(cur_year)).encode('utf-8')).hexdigest() }
                            res = cur.execute("SELECT date FROM festival_edition WHERE id_year = :id_year AND id_festival = :id_festival", params)
                            if res.fetchone() is None:
                                print("Adding to festival editions table: " + festival + ":" + str(cur_year))
                                cur.execute ("INSERT INTO festival_edition (id, id_festival, id_year, date, ticket_price, travel_price) VALUES (:id, :id_festival, :id_year, \"\", 0, 0)", params)
                                conn.commit()
                        except Exception as e:
                            print(e)
                            print("Unable to manage festival editions table")

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
                for presence in band.split(';'):
                    if presence.strip() == "1":
                        try:
                            params = {"id_artist" : hashlib.sha1(band_name.encode('utf-8')).hexdigest(), "id_festival" : festival_edition_ids[j] }
                            res = cur.execute("SELECT * FROM presences WHERE id_artist = :id_artist AND id_festival_edition = :id_festival", params)
                            if res.fetchone() is None:
                                print("Updating artist presences: " + band_name)
                                cur.execute("INSERT INTO presences (id_festival_edition, id_artist) VALUES (:id_festival, :id_artist)", params)
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

