from llama_index import Document
from pypdf import PdfReader
from loader.loader import Loader

'''
Strategy

Basically right now we're parsing one pdf document
object as a llama_index Document object. Ideally, I
would like to parse individual pages and process them
as nodes but I can't do this until I figure out a way,
to retrieve the correct Nodes from the index after
saving to disk. This shouldn't be too hard but I'd like
to this without creating a new file in the boot folder.
'''

class PDFLoader(Loader):
    def __init__(self, filepath: str) -> None:
        self.filepath = filepath

    def load_doc(self) -> Document | None:
        try:
            text = ""
            self.reader = PdfReader(self.filepath)
            for page in self.reader.pages:
                text += page.extract_text() + "\n"
            doc = Document(
                text=text
            )
            return doc
        except:
            return None

