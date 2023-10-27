import os

from loader.pdfloader import PDFLoader

def run():
    dirname = os.path.dirname(__file__)
    filepath = os.path.join(dirname, "data", "bitcoin.pdf")
    doc = PDFLoader(filepath).load_doc()
    if doc:
        print(doc.text)

if __name__ == "__main__":
    run()
