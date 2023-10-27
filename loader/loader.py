from abc import abstractmethod
from llama_index import Document

class Loader:
    def __init__(self) -> None:
        pass

    @abstractmethod
    def load_doc(self, filepath: str) -> Document:
        pass
