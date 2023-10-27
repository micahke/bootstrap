from typing import List
from llama_index import Document
from loader.pdfloader import PDFLoader

class CustomLoader:
    @classmethod
    def load_pdf(cls, filepath: str):
        return PDFLoader(filepath).load_doc()


    @classmethod
    def load(cls, filepath: str) -> Document | None:
        SUPPORTED = {
            ".pdf": cls.load_pdf
        }
        # Get the extension from the filepath
        extension: str = "." + filepath.split(".")[-1]
        # Check if the extension is supported
        if extension not in SUPPORTED:
            return None
            # raise RuntimeError(f"Extension {extension} is not supported")
        else:
            return SUPPORTED[extension](filepath)



