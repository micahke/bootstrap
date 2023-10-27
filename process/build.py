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


    def run(self, args: Any = None):
        files = FileWalker(self.config, ".").walk()
        current_snapshot = Snapshot.build(files)
        docs = []
        for file in files:
            doc = self.client.generate_doc(file)
            docs.append(doc)

        nodes = self.client.parse_nodes(docs)
        index = self.client.generate_index_from_nodes(nodes)
        self.client.save_index(index)
        print(f"Indexed {len(files)} file(s).")
        current_snapshot.save()
