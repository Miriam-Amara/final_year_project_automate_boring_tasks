#!/usr/bin/env python3

"""
This module implements functions to get a course material
metadata from the user.
"""

from pathlib import Path

from models.validatecoursemetadata import ValidateCourseMetadata

validate_data = ValidateCourseMetadata()

def get_department() -> str:
    while True:
        try:
            validate_data.department_code = input("\nEnter the department code: ")
            action = input("Are you sure? 'y or n': ").lower()
            if action == 'n':
                continue
            return validate_data.department_code
        except ValueError as e:
            print(e)

def get_level() -> str:
    while True:
        try:
            validate_data.level = input("\nEnter the level: ")
            action = input("Are you sure? 'y or n': ").lower()
            if action == 'n':
                continue
            return validate_data.level
        except ValueError as e:
            print(e)

def get_course_code() -> str:
    """
    Gets the course code from user.
    """
    while True:
        course_code = input("\nEnter the course code: ")
        action = input("Are you sure? 'y or n': ").lower()
        if action == 'n':
            continue
        try:
            validate_data.course_code = course_code
            return validate_data.course_code
        except ValueError as e:
            print(e)

def get_title() -> str:
    while True:
        course_title = input("\nEnter the title of the material: ").lower()
        action = input("Are you sure? 'y or n': ").lower()
        if action == 'n':
            continue
        return course_title

def get_semester() -> str:
    while True:
        try:
            validate_data.semester = input(
                "\nEnter the semester e.g 'first semester', 'second semester': ")
            action = input("Are you sure? 'y or n': ").lower()
            if action == 'n':
                continue
            return validate_data.semester
        except ValueError as e:
            print(e)

def get_scope_type() -> str:
    while True:
        try:
            validate_data.scope_type = input(
                "\nEnter the scope of the course "
                "e.g 'general', 'shared', 'departmental': ")
            action = input("Are you sure? 'y or n': ").lower()
            if action == 'n':
                continue
            return validate_data.scope_type
        except ValueError as e:
            print(e)

def get_content_type() -> str:
    while True:
        try:
            validate_data.content_type = input(
                "\nEnter the content type "
                "'note', 'material', 'textbook', 'past question': ")
            action = input("Are you sure? 'y or n': ").lower()
            if action == 'n':
                continue
            return validate_data.content_type
        except ValueError as e:
            print(e)

def get_original_file_path(fpath: str | Path) -> Path:
    """
    Returns file path.
    """
    if fpath:
        try:
            validate_data.file_path = fpath
            return validate_data.file_path
        except FileNotFoundError as e:
            print(e)

    while True:
        try:
            validate_data.file_path = input("\nEnter the folder path: ")
            action = input("Are you sure? 'y or n': ").lower()
            if action == 'n':
                continue
            return validate_data.file_path
        except FileNotFoundError as e:
            print(e)

def get_year() -> str:
    while True:
        try:
            validate_data.year = input("\nEnter year: ")
            action = input("Are you sure? 'y or n': ").lower()
            if action == 'n':
                continue
            return validate_data.year
        except ValueError as e:
            print(e)
