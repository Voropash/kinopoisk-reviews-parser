#!/usr/bin/python

def save(conn, review_item):
    print("Save info to DB")
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO reviews (reviewText, author, reviewdate, imageLink, imageBase64, filmName, infos, kpRating, kpRatingCount, imdbRating, actorList, alternativeheadline) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
        review_item)
    conn.commit()
    cur.close()
