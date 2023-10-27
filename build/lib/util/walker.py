import os
import re
from typing import List
from data.config import Config


class FileWalker:
    def __init__(self, config: Config, dir: str) -> None:
        self.config = config
        self.dir = dir
        self.filepaths = []



    def walk(self) -> List[str]:
        filepaths = []
        for dirpath, dirnames, filenames in os.walk(self.dir):
            base_dirname = os.path.basename(dirpath)
            if base_dirname in self.config.excluded_dirs:
                dirnames[:] = []
                continue
            for filename in filenames:
                if any(filename.endswith(ext) for ext in self.config.filetypes):
                    filepaths.append(os.path.join(dirpath, filename))  
        return filepaths



