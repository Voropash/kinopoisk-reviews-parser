#!/usr/bin/python
import base64
import json
import random
import time

import requests

from db_saver import save


def parse_one_review(driver, conn):
    driver.get("https://www.kinopoisk.ru/chance/")
    big_button = driver.find_element_by_class_name("button")
    big_button.click()
    time.sleep(0.5)
    file_name = driver.find_element_by_class_name("filmName")
    link_to_film = file_name.find_element_by_tag_name("a")
    link_to_film.click()
    print("Movie link:" + driver.current_url)

    header_film = driver.find_element_by_id("headerFilm")
    alternative_headline_block = header_film.find_element_by_tag_name("span")
    alternative_headline = alternative_headline_block.text
    reviews_menu = driver.find_element_by_class_name("resp_type")
    reviews_menu_links = reviews_menu.find_elements_by_tag_name("a")
    reviews_menu_all_link = reviews_menu_links[0]
    driver.execute_script("arguments[0].scrollIntoView();", reviews_menu_all_link)
    driver.execute_script("window.scrollBy(0, -50);", reviews_menu_all_link)
    reviews_menu_all_link.click()

    user_reviews = driver.find_elements_by_class_name("userReview")
    review_count = len(user_reviews)
    review_number = random.randrange(0, review_count, 1)
    user_review = user_reviews[review_number]
    review_block = user_review.find_element_by_class_name("_reachbanner_")
    review_text = review_block.get_attribute('innerHTML')
    review_text = review_text.replace("&nbsp;", " ") \
        .replace("<br>", "\n")

    # TODO: For markDown support
    # .replace("<b>", "**") \
    # .replace("</b>", "**") \
    # .replace("<i>", "__") \
    # .replace("</i>", "__")

    profile_name = user_review.find_element_by_class_name("profile_name")
    profile_name_link = profile_name.find_element_by_tag_name("a")
    author = profile_name_link.get_attribute('innerHTML')

    date_block = user_review.find_element_by_class_name("date")
    date = date_block.get_attribute('innerHTML')

    image_block = driver.find_element_by_class_name("popupBigImage")
    image_link = image_block.get_attribute("href")
    image_base64 = base64.b64encode(requests.get(image_link).content)

    film_name_block = driver.find_element_by_class_name("moviename-big")
    film_name = film_name_block.get_attribute('innerHTML')

    info_table = driver.find_element_by_id("infoTable")
    info_table_rows = info_table.find_elements_by_tag_name("tr")
    infos = []
    for infoTableRow in info_table_rows:
        columns = infoTableRow.find_elements_by_tag_name("td")
        row_name = columns[0]
        property_name = row_name.get_attribute('innerHTML')
        row_value = columns[1]
        property_value = row_value.text
        infos.append([property_name, property_value])
    infos_json = json.dumps(infos)

    kp_rating_block = driver.find_element_by_class_name("rating_ball")
    kp_rating = kp_rating_block.text
    kp_rating_count_block = driver.find_element_by_class_name("ratingCount")
    kp_rating_count = kp_rating_count_block.text

    rating_block = driver.find_element_by_class_name("block_2")
    rating_blocks = rating_block.find_elements_by_tag_name("div")
    imdb_block = rating_blocks[1]
    imdb_rating = imdb_block.text

    actor_list_block = driver.find_element_by_id("actorList")
    actor_list_block_list = actor_list_block.find_element_by_tag_name("ul")
    actor_list = actor_list_block_list.text

    review_item = (
        review_text,
        author,
        date,
        image_link,
        image_base64,
        film_name,
        infos_json,
        kp_rating,
        kp_rating_count,
        imdb_rating,
        actor_list,
        alternative_headline)

    save(conn, review_item)
