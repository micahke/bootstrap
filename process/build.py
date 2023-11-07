from typing import Any
from llama_index.llms import OpenAI 
from data.config import Config
from data.snapshot import Snapshot
from llm.llama_index import LlamaClient
from process.process import Process
from util.walker import FileWalker
from llama_index.evaluation import DatasetGenerator

class BuildProcess(Process):
    def __init__(self, config: Config, client: LlamaClient) -> None:
        super().__init__()
        self.config = config
        self.client = client


    def run(self, args: Any = None):
        if args.verbose:
            self.config.set_verbose(True)
        files = FileWalker(self.config, ".").walk()
        current_snapshot = Snapshot.build(files)
        docs = []
        for file in files:
            doc = self.client.generate_doc(file)
            docs.append(doc)
            print(f"Added {file.strip('./')}")

        if args.summary:
            self.summary(docs, args.verbose)

        nodes = self.client.parse_nodes(docs)
        llm = OpenAI(model=self.config.llm_params.model_type.value[1], temperature=self.config.temperature, max_tokens=self.config.max_tokens)
        index = self.client.generate_index_from_nodes(llm, self.config.index_params.index_type, nodes, self.config.index_params.verbose)
        self.client.save_index(index)
        print(f"Indexed {len(files)} file(s).")
        current_snapshot.save()


    def summary(self, docs, verbose):
        data_generator = DatasetGenerator.from_documents(docs, show_progress=verbose)
        eval_questions = data_generator.generate_questions_from_nodes()
        output = ""
        for q in eval_questions:
            output += q +"\n"
        with open("summary.txt", "w") as file:
            file.write(output)

