import hashlib
from typing import List
import json
from util.fs import get_snapshot_filepath


class Snapshot:
    def __init__(self) -> None:
        self.items = {}
    
    def add_item(self, filepath: str, hash: str):
        self.items[filepath] = hash  

    def save(self):
        fp = get_snapshot_filepath()
        with open(fp, "w") as file:
            json.dump(self.items, file)

    @classmethod
    def load(cls):
        fp = get_snapshot_filepath()
        with open(fp, 'r') as file:
            items = json.loads(file.read())
        snapshot = Snapshot()
        snapshot.items = items
        return snapshot

    @classmethod
    def hash_file(cls, filepath: str) -> str:
        hash = hashlib.sha256()
        with open(filepath, "rb") as file:
            for block in iter(lambda: file.read(4096), b""):
                hash.update(block)
        return hash.hexdigest()

    @classmethod
    def build(cls, files: List[str]):
        snapshot = Snapshot()
        for filepath in files:
            hash = cls.hash_file(filepath)
            snapshot.add_item(filepath, hash)
        return snapshot
    

    @classmethod
    def compare(cls, old: 'Snapshot', new: 'Snapshot') -> tuple[List[str], List[str], List[str]]:
        _new = []
        _updated =  []
        _deleted = []

        # find new and updated files
        for file_path, new_hash in new.items.items():
            old_hash = old.items.get(file_path)
            if old_hash is None:
                _new.append(file_path)
            elif old_hash != new_hash:
                _updated.append(file_path)

        # find deleted files
        for file_path in old.items.keys():
            if file_path not in new.items:
                _deleted.append(file_path)

        return _new, _updated, _deleted

