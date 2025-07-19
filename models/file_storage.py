#!/usr/bin/env python3

"""
Stores the metadata of course materials into file storage.
"""

from dotenv import load_dotenv
from typing import Any
import json
import os

from models.organize_files import OrganizeFile

load_dotenv()

class FileStorage:
    __filepath: str = ""
    __objects: dict[str, Any] = {}
    __file_storage: str = os.getenv("FILE_STORAGE", "course_materials_storage.json")

    def all(self) -> str:
        """
        Returns all objects of OrganizeFile
        """
        return FileStorage.__filepath
    
    def new(self, obj: OrganizeFile) -> None:
        """
        Adds a new object of OrganizeFile into __objects dictionary.
        """
        key = f"{obj.course_code}.{obj.id}"
        FileStorage.__objects[key] = obj

    def save(self) -> None:
        """
        Serializes object dict to file storage.
        """
        obj_dict = {}
        with open(FileStorage.__file_storage, "w") as file_obj:
            for key, obj in FileStorage.__objects.items():
                obj_dict[key] = obj.to_dict()
            json.dump(obj_dict, file_obj, indent=4)


    def reload(self) -> None:
        """
        Deserializes from json to python dict.
        """
        if not FileStorage.__file_storage:
            raise TypeError(f"{FileStorage.__file_storage} is does not exist")
        try:
            with open(FileStorage.__file_storage) as file_obj:
                all_objects = json.load(file_obj)
        except json.decoder.JSONDecodeError:
            pass
        else:
            for key, kwargs in all_objects.items():
                file_path = kwargs["original_file_path"]
                new_file_obj = OrganizeFile(file_path, **kwargs)
                FileStorage.__objects[key] = new_file_obj
