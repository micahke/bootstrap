from llama_index import Document
from loader.loader import Loader
from docx import Document as Docx


class DocxLoader(Loader):
    def __init__(self, filepath: str) -> None:
        self.filepath = filepath

    def load_doc(self) -> Document | None:
        try:
            data = []
            word_doc = Docx(self.filepath)
            for paragraph in word_doc.paragraphs:
                data.append(paragraph.text)
            text = '\n'.join(data)
            doc = Document(
                text=text
            )
            return doc
        except:
            return None

