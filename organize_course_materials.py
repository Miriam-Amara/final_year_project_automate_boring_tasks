#!/usr/bin/env python3

"""
A script that automates downloading
google drive files and folders

1. Extract files and folders
2. Rename them
3. Group them by format (e.g pdf, png, mp4, pptx)
4. Put everything in one folder depending on the semester (e.g first semester)
5. Put everything in one folder depending on the level (e.g 500 level)
6. Upload to google drive

1. Enter the file path, zipfile name, department and level
2. Verify info above
    - Check if filename exists and file is a zip file
    - Check if department name is valid
    - Check if level is valid
3. Extract file
4. Check folder structure
    - If it is a folder
        - prompt the folders name
        - prompt to move or rename
    - If it is a file
        - prompt the file name
        - prompt to move or rename
3. Group them by format (e.g pdf, png, mp4, pptx)
"""


import logging
import shutil
import sys
from zipfile import is_zipfile, ZipFile
from pathlib import Path
from typing import Any


logging.basicConfig(
    level=logging.DEBUG,
    format=" %(asctime)s - %(levelname)s - %(message)s",
    filename="course_materials.log"
)

disable_logging = False
if disable_logging:
    logging.disable(logging.CRITICAL)


def file_information() -> dict[str, str]:
    """
    
    """
    file_info = {}
    file_name = input("Enter the name of the zipfile:\n")
    department = input("Enter the name of the department:\n")
    level = input("Enter the level:\n")

    file_info["file_name"] = file_name
    file_info["department"] = department
    file_info["level"] = level
    return file_info


class VerifyInfo:
    """
    
    """
    def __init__(self,
                 file_name: Any,
                 department_name: str,
                 level: str
                 ) -> None:
        self.file_name = file_name
        self.department_name = department_name
        self.level = level
        if not self.file_name:
            raise Exception("File name cannot be empty")
        if not self.department_name:
            raise Exception("Department name cannot be empty")
        if not self.level:
            raise Exception("Level cannot be empty")
        self.folder_path: Any = Path("/mnt/c/Users/Precision/Downloads")
        self.file_path: Any = self.folder_path / self.file_name

    def file_path_exists(self) -> None:
        """
        Checks whether the given file path and file exits.
        Raises an exception if file_path and file does not exist.
        """
        if not self.folder_path.exists():
            raise Exception(f"File path: {self.folder_path} does not exists")
        if not self.file_path.exists():
            raise Exception(f"File {self.file_name} "
                            f"does not exist in {self.folder_path}")
        
    
    def is_zipfile(self) -> bool:
        """
        Checks whether file exists and is a zip file.
        """
        return self.file_path.is_zipfile()
        
    def is_department(self) -> bool:
        """
        Checks whether department name is valid
        """
        department_codes: dict[str, str] = {
            "age": "agricultural engineering",
            "che": "chemical engineering",
            "cve": "civil engineering",
            "cpe": "computer engineering",
            "eee": "electrical engineering",
            "ide": "industrial engineering",
            "mre": "marine engineering",
            "mme": "material and metallurgy engineering",
            "mee": "mechanical engineering",
            "mte": "mechatronics engineering",
            "pre": "production engineering",
            "pee": "petroleum engineering",
            "ste": "structural engineering"
        }
        if (self.department_name.lower() in department_codes.values()):
            return True
        else:
            return False
    
    def is_level(self) -> bool:
        """
        Checks whether level is valid.
        """
        levels: dict[int, str] = {
            1: "100",
            2: "200",
            3: "300",
            4: "400",
            5: "500"
        }
        if self.level in levels.values():
            return True
        else:
            return False




def unzip_files() -> None:
    """
    
    """



logging.debug("Start program")


downloads = Path("/mnt/c/Users/Precision/Downloads")
docx_folder = downloads / "DOCX_files"
pdf_folder = downloads / "PDF_files"
pptx_folder = downloads / "PPTX_files"
mp4_folder = downloads / "MP4_files"
image_folder = downloads / "IMAGES"
docx_folder.mkdir(exist_ok=True)
pdf_folder.mkdir(exist_ok=True)
pptx_folder.mkdir(exist_ok=True)
mp4_folder.mkdir(exist_ok=True)
image_folder.mkdir(exist_ok=True)

docx = Path("/mnt/c/Users/Precision/Downloads/DOCX_files")
pdfs = Path("/mnt/c/Users/Precision/Downloads/PDF_files")
pptx = Path("/mnt/c/Users/Precision/Downloads/PPTX_files")
mp4 = Path("/mnt/c/Users/Precision/Downloads/MP4_files")
images = Path("/mnt/c/Users/Precision/Downloads/IMAGES")

for file in downloads.iterdir():
    if file.is_file():
        if str(file.name).endswith("docx"):
            shutil.move(str(file), str(docx / file.name))
        elif str(file.name).endswith("pdf"):
            shutil.move(str(file), str(pdfs / file.name))
        elif str(file.name).endswith("pptx"):
            shutil.move(str(file), str(pptx / file.name))
        elif str(file.name).endswith("mp4"):
            shutil.move(str(file), str(mp4 / file.name))
        elif str(file.name).endswith((".jpg", ".jpeg", ".png")):
            shutil.move(str(file), str(images / file.name))
