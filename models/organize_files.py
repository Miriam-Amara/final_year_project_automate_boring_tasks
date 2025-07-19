#!/usr/bin/env python3

"""

"""
from copy import deepcopy
from datetime import datetime
from uuid import uuid4
from pathlib import Path
from typing import Any
import json

from models.get_user_input import get_content_type, get_course_code, get_department
from models.get_user_input import get_level, get_original_file_path, get_scope_type
from models.get_user_input import get_semester, get_title, get_year

class OrganizeFile:
    """
    
    """
    def __init__(self, file_path: str | Path, **kwargs: Any) -> None:
        if "created_at" in kwargs:
            kwargs["created_at"] = datetime.fromisoformat(kwargs["created_at"])
            kwargs["updated_at"] = datetime.fromisoformat(kwargs["updated_at"])
            self.__dict__.update(kwargs)
        else:
            self.id = str(uuid4())[0:8]
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
            self.department: str = get_department()
            self.level:str = get_level()
            self.course_code: str = get_course_code()
            self.scope_type: str = get_scope_type()
            self.title: str = get_title()
            self.semester: str = get_semester()
            self.content_type: str = get_content_type()
            self.year: str = get_year()
            self.original_file_path: Path = get_original_file_path(file_path)
            self.new_file_path: Path = Path("")
            self.filename: str = ""
            self.__dict__.update(kwargs)
            from models import storage
            storage.new(self)
    
    def generate_file_name(self) -> None:
        """
        Renames a file.
        """
        file_format = self.original_file_path.suffix
        if self.year:
            self.filename = (f"{self.course_code}_{self.content_type}_"
                        f"{self.year}_{self.id}{file_format}")
        else:
            self.filename = (f"{self.course_code}_{self.content_type}_"
                        f"{self.id}{file_format}")
            
    def rename_file(self, new_folder: Path):
        """
        Moves file to a new file path
        """
        self.new_file_path = new_folder
        print(f"{self.original_file_path.name} will be renamed to {self.filename}")
        destination = new_folder / self.filename
        self.original_file_path.replace(destination)
        # shutil.copy2(self.original_file_path, destination)

    def generate_s3_path(self) -> None:
        """
        Moves file to a folder in aws s3 bucket
        """
        if self.scope_type == "shared" or self.scope_type == "general":
            self.s3_path = (f"{self.level}_level/{self.scope_type}/"
                                f"{self.semester}/{self.filename}")
        elif self.scope_type == "departmental":
            self.s3_path = (f"{self.level}_level/departments/{self.department}/"
                                f"{self.semester}/{self.filename}")

    def __str__(self) -> str:
        obj_dict_copy = deepcopy(self.__dict__)
        obj_dict_copy["created_at"] = self.created_at.isoformat()
        obj_dict_copy["updated_at"] = self.updated_at.isoformat()
        obj_dict_copy["original_file_path"] = str(self.original_file_path)
        obj_dict_copy["new_file_path"] = str(self.new_file_path)
        return (f"[{self.course_code}]({self.id})"
                f"({json.dumps(obj_dict_copy, indent=4)})")
        
    def save(self) -> None:
        self.updated_at = datetime.now()
        from models import storage
        storage.save()

    def to_dict(self) -> dict[str, dict[str, Any]]:
        """
        Returns a serializable dict format of the object.
        """
        obj_dict_copy = deepcopy(self.__dict__)
        obj_dict_copy["created_at"] = self.created_at.isoformat()
        obj_dict_copy["updated_at"] = self.updated_at.isoformat()
        obj_dict_copy["original_file_path"] = str(self.original_file_path)
        obj_dict_copy["new_file_path"] = str(self.new_file_path)
        return obj_dict_copy
