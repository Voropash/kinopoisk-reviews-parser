#!/usr/bin/python
import random
import sys
import time
import traceback

import psycopg2
from selenium import webdriver

from review_getter import parse_one_review

MAX_ITERATIONS = 100000


def init(argv):
    sleep_period_s = 0
    iterations = 99999

    if len(argv) > 2:
        sleep_period_s = argv[2]
    if len(argv) > 1:
        iterations = argv[1]

    random.seed()
    driver = webdriver.Chrome('chromedriver.exe')
    # driver = webdriver.PhantomJS('phantomjs.exe')

    parse(driver, iterations, sleep_period_s)
    driver.quit()


def parse(driver, iterations, sleep_period_s):
    for x in range(0, iterations):
        try:
            print("Start getting " + str(x + 1) + " review")
            parse_one_review(driver)
            print("Successful parsing")
            time.sleep(sleep_period_s)
        except Exception:
            print("Parsing error:")
            print("-" * 60)
            traceback.print_exc(file=sys.stdout)
            print("-" * 60)
    print("Parsing successful completed")


if __name__ == "__main__":
    sys.exit(init(sys.argv))
