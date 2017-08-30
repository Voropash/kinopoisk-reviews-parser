#!/usr/bin/python
import sys

import psycopg2


def createPgTable():
    conn = psycopg2.connect("dbname=kp user=kp password=kp")
    cur = conn.cursor()
    cur.execute(
        "CREATE TABLE reviews (id serial PRIMARY KEY, reviewText varchar, author varchar, reviewdate varchar, imageLink varchar, imageBase64 bytea, filmName varchar, infos varchar, kpRating varchar, kpRatingCount varchar, imdbRating varchar, actorList varchar, alternativeHeadline varchar);")
    conn.commit()
    cur.close()
    conn.close()


if __name__ == "__main__":
    sys.exit(createPgTable())
