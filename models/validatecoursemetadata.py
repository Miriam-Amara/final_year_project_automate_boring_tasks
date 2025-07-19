#!/usr/bin/env python3

"""
This module contains validation for course materials metadata.
"""

import logging
from pathlib import Path


logging.basicConfig(
    level=logging.DEBUG,
    format=" %(asctime)s - %(levelname)s - %(message)s",
    filename="models.log",
)

disable_logging: bool = False
if disable_logging:
    logging.disable(logging.CRITICAL)

class ValidateCourseMetadata:
    """
    This class validates user inputs for the various metadata of
    a course material.
    """
    def __init__(self) -> None:
        self._scope_types = ["general", "shared", "departmental"]
        self._dept_codes = [
            "GENERAL", "AGE", "CHE", "CVE", "CPE", "EEE", "IDE",
            "MEE", "MME", "MTE", "MRE", "PEE", "PRE", "STE", "CED"
        ]
        self._levels: list[str] = ["100", "200", "300", "400", "500"]
        self._scope_type: str = ""
        self._department_code: str = ""
        self._level: str = ""
        self._course_code: str = ""
        self._file_path: Path = Path("")
        self._content_type: str = ""
        self._semester: str = ""
        self._year: str = ""
    
    @property
    def scope_type(self) -> str:
        return self._scope_type
    
    @scope_type.setter
    def scope_type(self, scopetype: str) -> None:
        scopetype = scopetype.strip().lower()
        if scopetype not in self._scope_types:
            raise ValueError(f"{scopetype} not valid.\n"
                             "These are the types available: "
                             "general, shared, departmental")
        self._scope_type = scopetype
    
    @property
    def department_code(self) -> str:
        return self._department_code
    
    @department_code.setter
    def department_code(self, dept_code: str) -> None:
        dept_code = dept_code.strip().upper()
        if dept_code not in self._dept_codes:
            raise ValueError(f"{dept_code} is not a valid department code.\n"
                             "These are the department codes available:\n"
                             "AGE, CHE, CVE, CPE, EEE, IDE, MEE, MME, MTE, MRE, "
                             "PEE, PRE, STE, CED")
        self._department_code = dept_code
    
    @property
    def level(self) -> str:
        return self._level
    
    @level.setter
    def level(self, lvl: str) -> None:
        if lvl.strip() not in self._levels:
            raise ValueError(f"{lvl} not a valid level.\n"
                             "These are the levels available: "
                             "100, 200, 300, 400, 500")
        self._level = lvl
    
    @property
    def course_code(self) -> str:
        return self._course_code
    
    @course_code.setter
    def course_code(self, coursecode: str) -> None:
        coursecode = coursecode.strip().upper()
        if len(coursecode) != 6:
            raise ValueError(f"{coursecode} is invalid.\n"
                             "Ensure to type the correct course code e.g IDE551 "
                             "with no spaces.")
        dept_code = coursecode[:3]
        if dept_code not in self._dept_codes:
            raise ValueError(f"{dept_code} in {coursecode} is not a valid department code.\n"
                             "These are the department codes available:\n"
                             "AGE, CHE, CVE, CPE, EEE, IDE, MEE, MME, MTE, MRE, "
                             "PEE, PRE, STE", "CED")

        if coursecode[3] != self._level[0]:
            raise ValueError(f"{coursecode[3:]} in {coursecode} is not a course code "
                             f"for {self._level} level.")
        self._course_code = coursecode
    
    @property
    def file_path(self) -> Path:
        return self._file_path
    
    @file_path.setter
    def file_path(self, fpath: str | Path) -> None:
        if isinstance(fpath, str):
            fpath.strip()
        filepath = Path(fpath)
        if not filepath.exists():
            raise FileNotFoundError(f"{filepath} does not exist.")
        self._file_path = filepath
    
    @property
    def content_type(self) -> str:
        return self._content_type
    
    @content_type.setter
    def content_type(self, ctype: str) -> None:
        content_types = {
            "note": "note",
            "textbook": "textbook",
            "material": "material",
            "past question": "past_question",
        }
        ctype = ctype.strip().lower()
        if ctype not in content_types:
            raise ValueError(f"{ctype} is not available.\n"
                             "These are the available types: "
                             "note, textbook, lecturer material, "
                             "past question")
        self._content_type = content_types[ctype]
    
    @property
    def semester(self) -> str:
        return self._semester
    
    @semester.setter
    def semester(self, semstr: str) -> None:
        semesters = {
            "first semester": "first_semester",
            "second semester": "second_semester"
            }
        semstr = semstr.strip().lower()
        if semstr not in semesters:
            raise ValueError(f"{semstr} not found.\n"
                             "These are the semesters available: "
                             "first semester, second semester.")
        self._semester = semesters[semstr]
    
    @property
    def year(self) -> str:
        return self._year
    
    @year.setter
    def year(self, yr: str):
        if yr:
            yr = yr.strip()
            if not yr.isdigit():
                raise ValueError(f"{yr} is not a vaild year.\n"
                                "Expects values like '2015, 2010, 2024'.")
            
            if int(yr) < 2010 or int(yr)  > 2100:
                raise ValueError(f"{yr} is not a valid year.\n"
                                "Expects values from 2010 to 2100.")
        self._year = yr
