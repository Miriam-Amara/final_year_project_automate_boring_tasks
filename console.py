#!/usr/bin/python3

"""

"""

from cmd import Cmd
from pathlib import Path

# from models import storage
from models.organize_files import OrganizeFile


class UnibenEngVault(Cmd):
    """
    
    """
    Cmd.prompt = "(UnibenEngVault) "
    __original_folder_path: Path = Path("")
    new_folder_path: Path | str = ""

    def preloop(self):
        print("""
    Welcome to UnibenEngVault.
    This programs renames and upload course materials
    to cloud storage AWS s3 bucket.
    Enter the folder path to continue\n
    """)
        
    def postloop(self):
        print("Bye!")

    def emptyline(self):
        return False
    
    def do_quit(self, args: str):
        return True
    
    def do_EOF(self, args: str):
        return True
    
    def parse_files(self):
        """
        Parses all files in a given folder.
        """
        original_folder_path: Path = UnibenEngVault.__original_folder_path
        formats = [".pdf", ".jpg", ".jpeg", ".png", ".pptx"]
        invalid_files: list[str] = []

        if (not UnibenEngVault.new_folder_path
            or not isinstance(UnibenEngVault.new_folder_path, Path)):
            print("\nPlease specify a new folder path.")
            return
        
        print("\n\tRenaming of files has started."
              f"\n\tAll files will be moved into {UnibenEngVault.new_folder_path}"
              "\n\tIf you make a mistake enter 'n' to redo the process."
              "\n\tGoodluck!\n")
        for item in original_folder_path.rglob('*'):
            if not item.is_file():
                continue
            if item.suffix.lower() not in formats:
                invalid_files.append(item.name)
            
            action = input(f"\n\t***File name - {item.name}."
                           " (Do you want to skip this file? 'y' or 'n': ")
            if action.strip().lower() == "y":
                continue
            try:
                new_file = OrganizeFile(item)
            except EOFError:
                print()
                return
            new_file.generate_file_name()
            new_file.rename_file(UnibenEngVault.new_folder_path)
            new_file.generate_s3_path()
            new_file.save()
            print("\n", str(new_file))
            

        if invalid_files:
            print("\nThese files were not renamed.")
            for file in invalid_files:
                print(file)
    
    def do_new_folder(self, args: str) -> None | Path:
        """
        
        """
        if not args:
            print("Folder name must not be empty.")
            return
        
        new_folder = args.strip()
        UnibenEngVault.new_folder_path = Path(new_folder)
        if UnibenEngVault.new_folder_path.exists():
            print(f"{str(UnibenEngVault.new_folder_path)} already exists.")
        else:
            UnibenEngVault.new_folder_path.mkdir()
        UnibenEngVault.new_folder_path

    def do_folder(self, args: str) -> None:
        """
        Checks if a folder path exists.        
        """
        if not args:
            print("No folder path given")
            return
        
        folder = args.strip()
        folder_path = Path(args)
        if not folder_path.exists():
            print(f"{folder} does not exist")
            return
        
        if not folder_path.is_dir():
            print(f"{folder} is not a folder")
            return
        
        UnibenEngVault.__original_folder_path = folder_path
        self.parse_files()
    
    def do_show(self, args: str):
        """
        
        """
        pass


if __name__ == "__main__":
    UnibenEngVault().cmdloop()
