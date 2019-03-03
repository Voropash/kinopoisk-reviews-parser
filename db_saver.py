#!/usr/bin/python
import psycopg2

def save(review_item):
    print("Save info to DB")
    conn = psycopg2.connect("dbname=kp user=kp password=kp port=5434")
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO reviews (reviewText, author, reviewdate, imageLink, imageBase64, filmName, infos, kpRating, kpRatingCount, imdbRating, actorList, alternativeheadline) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
        review_item)
    conn.commit()
    conn.close()
    cur.close()
