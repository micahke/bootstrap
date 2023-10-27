from typing import Optional, List

class Config:
    def __init__(self, name: Optional[str] = "") -> None:
        self.name = name
        self.description = ""
        self.filetypes: List[str] = []
        self.excluded_dirs: List[str] = []

    def set_name(self, name: str):
        self.name = name

    def set_description(self, description: str):
        self.description = description

    def set_filetypes(self, filetypes: List[str]):
        self.filetypes = filetypes

    def set_excluded_dirs(self, excluded_dirs: List[str]):
        self.excluded_dirs = excluded_dirs


