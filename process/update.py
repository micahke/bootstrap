import hashlib
from typing import Any, List

from llama_index import PromptHelper
from llama_index.bridge.langchain import OpenAI
from data.config import Config
from data.snapshot import Snapshot
from llm.llama_index import LlamaClient
from process.process import Process
from util.fs import snapshot_exists
from util.walker import FileWalker

class UpdateProcess(Process):
    def __init__(self, config: Config, client: LlamaClient) -> None:
        super().__init__()
        self.config = config
        self.client = client

    def update_index(self, new: List[str], updated: List[str], deleted: List[str]):
        llm = OpenAI(model=self.config.llm_params.model_type.value[1], temperature=self.config.temperature, max_tokens=self.config.max_tokens)
        prompt_helper = PromptHelper(
          context_window=self.config.llm_params.model_type.value[2],
          num_output=self.config.max_tokens or 512,
          chunk_overlap_ratio=0.5,
          chunk_size_limit=None
        )
        index = self.client.load_index(llm, promptHelper=prompt_helper)
        docs = []
        for file in new:
            doc = self.client.generate_doc(file)
            docs.append(doc)
            print(f"Added {file.strip('./')}")

        print(f"Added {len(new)} file(s).")
        for file in updated:
            hash = hashlib.md5(file.encode()).hexdigest()
            try:
                index.delete_ref_doc(hash)
            except:
                # One of the nodes already removed
                pass

            doc = self.client.generate_doc(file)
            docs.append(doc)
            print(f"Updated {file.strip('./')}")

        print(f"Updated {len(updated)} file(s).")
        nodes = self.client.parse_nodes(docs)
        index.insert_nodes(nodes)
        
        for file in deleted:
            hash = hashlib.md5(file.encode()).hexdigest()
            try:
                index.delete_ref_doc(hash)
                print(f"Deleted {file.strip('./')}")
            except:
                # One of the nodes already removed
                pass
        if len(deleted) > 0:
            print(f"Deleted {len(deleted)} file(s).")
        self.client.save_index(index)


    def run(self, args: Any = None):
        files = FileWalker(self.config, ".").walk()
        current_snapshot = Snapshot.build(files)
        if snapshot_exists():
            old_snapshot = Snapshot.load()
            new, updated, deleted = Snapshot.compare(old_snapshot, current_snapshot)
            self.update_index(new, updated, deleted)
            current_snapshot.save()
        else:
            print("Please run `bootstrap build` first.")
