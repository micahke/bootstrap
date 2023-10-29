from dataclasses import dataclass
from enum import Enum
from typing import Literal, Optional, List

class IndexType(Enum):
    VECTOR =  "vector"
    TREE = "tree"

@dataclass
class ConfigIndexParams:
    index_type: IndexType
    verbose: bool

class Config:
    def __init__(self, name: Optional[str] = "") -> None:
        self.name = name
        self.description = ""
        self.filetypes: List[str] = []
        self.excluded_dirs: List[str] = []
        self.index_params = ConfigIndexParams(index_type=IndexType.VECTOR, verbose=False)

    def set_name(self, name: str):
        self.name = name

    def set_description(self, description: str):
        self.description = description

    def set_filetypes(self, filetypes: List[str]):
        self.filetypes = filetypes

    def set_excluded_dirs(self, excluded_dirs: List[str]):
        self.excluded_dirs = excluded_dirs


    def set_index_type(self, index_type: IndexType):
        self.index_params.index_type = index_type

    def set_verbose(self, verbose: bool):
        self.index_params.verbose = verbose
