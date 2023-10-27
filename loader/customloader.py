from llama_index import Document
from loader.docxloader import DocxLoader
from loader.pdfloader import PDFLoader

class CustomLoader:
    @classmethod
    def load_pdf(cls, filepath: str):
        return PDFLoader(filepath).load_doc()

    @classmethod
    def load_docx(cls, filepath: str):
        return DocxLoader(filepath).load_doc()


    @classmethod
    def load(cls, filepath: str) -> Document | None:
        SUPPORTED = {
            ".pdf": cls.load_pdf,
            ".docx": cls.load_docx,
        }
        # Get the extension from the filepath
        extension: str = "." + filepath.split(".")[-1]
        extension = extension.lower()
        # Check if the extension is supported
        if extension not in SUPPORTED:
            return None
            # raise RuntimeError(f"Extension {extension} is not supported")
        else:
            return SUPPORTED[extension](filepath)



