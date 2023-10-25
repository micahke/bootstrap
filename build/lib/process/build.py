from typing import Any
from data.config import Config
from llm.llama_index import LlamaClient
from process.process import Process
from util.walker import FileWalker

class BuildProcess(Process):
    def __init__(self, config: Config, client: LlamaClient) -> None:
        super().__init__()
        self.config = config
        self.client = client

    def run(self, args: Any = None):
        files = FileWalker(self.config, ".").walk()
        docs = []
        for file in files:
            docs.append(self.client.generate_doc(file))

        nodes = self.client.parse_nodes(docs)
        index = self.client.generate_index_from_nodes(nodes)
        self.client.save_index(index)
