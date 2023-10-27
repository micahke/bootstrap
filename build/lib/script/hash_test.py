import hashlib
import os

def run():
    dirname = os.path.dirname(__file__)
    hash = hashlib.sha256()
    with open(os.path.join(dirname, "data/textfile.txt"), 'rb') as file:
        for block in iter(lambda: file.read(4096), b""):
            hash.update(block)
    print(hash.hexdigest())


if __name__ == "__main__":
    run()
