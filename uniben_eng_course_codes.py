#!/usr/bin/env python3

"""
This module scrapes information on course codes and course outlines
for each department and level in Engineering from the
University of Benin website.
"""

import sys
import logging
import requests
from http import HTTPStatus
from bs4 import BeautifulSoup

disable_logging = False

if disable_logging:
    logging.disable(logging.CRITICAL)

logging.basicConfig(
    level=logging.DEBUG,
    format=' %(asctime)s - %(levelname)s - %(message)s',
    filename='uniben_eng.log'
)
logging.debug("Start of program")

url = sys.argv[1]
course_name = sys.argv[2:]
logging.debug(course_name)
ide_response = requests.get(url)
code = ide_response.status_code
description = HTTPStatus(code).phrase

if ide_response.status_code != 200:
    raise Exception(f"{code} - {description}")

web_page = BeautifulSoup(ide_response.text, "lxml")
t_rows = web_page.select("tr")
span_tag = web_page.select("span")
levels = []

for span in span_tag:
    if "Table" in str(span):
        levels.append(span.get_text())
logging.debug(levels)

with open("eng_courses.txt", "a", encoding="utf-8") as f:
    course_name = " ".join(course_name)
    print(f"\n{course_name.upper()}\n{url}\n", file=f)
    for row in t_rows:
        logging.debug(row)
        td_semester = row.select("td")[0]
        try:
            td_course_code = row.select("td")[1]
            logging.debug(f"Course code {td_course_code.get_text()}")
        except IndexError as e:
            print(f"Error: {e}\nIt's no longer a table.", file=f)
            sys.exit()

        if "1st" in td_semester.get_text().lower():
            print("First Semester", file=f)
        elif "course code" in td_course_code.get_text().lower():
            logging.debug(f"First Course code in {td_course_code.get_text()}")
            course_code = "Course Code"
        elif "2nd" in td_semester.get_text().lower():
            print("Second Semester", file=f)
        else:
            td_course_code = row.select("td")[0]
        
        course_code = td_course_code.get_text()
        td_credit_load = row.select("td")[-1]
        course_credit_load = td_credit_load.get_text()
        print(f"{course_code}\t\t\t\t\t\t{course_credit_load}", file=f)
  
logging.debug("End of program")
