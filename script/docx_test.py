import os
from docx import Document

def pre_bootstrap(filepath):
    doc = Document(filepath)
    data = []
    for paragraph in doc.paragraphs:
        data.append(paragraph.text)
        # if paragraph.style.name == 'Heading 1':
        #     data.append(('Heading 1', paragraph.text))
        # elif paragraph.style.name == 'Heading 2':
        #     data.append(('Heading 2', paragraph.text))
        # else:
        #     data.append(('Normal', paragraph.text))
    text = '\n'.join(data)

def run():
    dirname = os.path.dirname(__file__)
    filepath = os.path.join(dirname, "data", "sample.docx")
    pre_bootstrap(filepath)
    

if __name__ == "__main__":
    run()
