from abc import abstractmethod
from concurrent.futures import ThreadPoolExecutor
import os
import re
from typing import List, Protocol
from data.config import Config

class Walker(Protocol):
    @abstractmethod
    def walk() -> List[str]:
        pass


class FileWalker(Walker):
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


class FileWalkerMultiThreaded(Walker):
    def __init__(self, config: Config, dir: str) -> None:
        self.config = config
        self.dir = dir
        self.filepaths = []

    def process_directory(self, dirpath, dirnames, filenames):
        base_dirname = os.path.basename(dirpath)
        if base_dirname in self.config.excluded_dirs:
            dirnames[:] = []
            return
        for filename in filenames:
            if any(filename.endswith(ext) for ext in self.config.filetypes):
                self.filepaths.append(os.path.join(dirpath, filename))

    def walk(self) -> List[str]:
        with ThreadPoolExecutor(max_workers=4) as executor:
            for dirpath, dirnames, filenames in os.walk(self.dir):
                executor.submit(self.process_directory, dirpath, dirnames, filenames)
        return self.filepaths
