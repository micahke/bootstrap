import hashlib
from typing import Any, List
from data.config import Config
from data.snapshot import Snapshot
from llm.llama_index import LlamaClient
from process.process import Process
from util.fs import snapshot_exists
from util.walker import FileWalker

class BuildProcess(Process):
    def __init__(self, config: Config, client: LlamaClient) -> None:
        super().__init__()
        self.config = config
        self.client = client

    def update_index(self, new: List[str], updated: List[str], deleted: List[str]):
        index = self.client.load_index()
        docs = []
        for file in new:
            doc = self.client.generate_doc(file)
            docs.append(doc)

        for file in updated:
            hash = hashlib.md5(file.encode()).hexdigest()
            try:
                index.delete_ref_doc(hash)
            except:
                # One of the nodes already removed
                pass

            doc = self.client.generate_doc(file)
            docs.append(doc)

        nodes = self.client.parse_nodes(docs)
        index.insert_nodes(nodes)
        
        for file in deleted:
            hash = hashlib.md5(file.encode()).hexdigest()
            try:
                index.delete_ref_doc(hash)
            except:
                # One of the nodes already removed
                pass
        self.client.save_index(index)


    def run(self, args: Any = None):
        files = FileWalker(self.config, ".").walk()
        current_snapshot = Snapshot.build(files)
        if snapshot_exists():
            old_snapshot = Snapshot.load()
            new, updated, deleted = Snapshot.compare(old_snapshot, current_snapshot)
            self.update_index(new, updated, deleted)
        else:
            docs = []
            for file in files:
                doc = self.client.generate_doc(file)
                docs.append(doc)

            nodes = self.client.parse_nodes(docs)
            index = self.client.generate_index_from_nodes(nodes)
            self.client.save_index(index)
        current_snapshot.save()
