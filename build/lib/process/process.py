from abc import abstractmethod
from typing import Any

class Process:
    def __init__(self) -> None:
        pass
    
    @abstractmethod
    def run(self, args: Any):
        pass
