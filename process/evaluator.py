import json
from typing import Any, List
from llama_index.llms import OpenAI
from llama_index import Document, ServiceContext, VectorStoreIndex
from llama_index.evaluation import DatasetGenerator, RelevancyEvaluator
from data.config import Config
from llm.llama_index import LlamaClient
from process.process import Process
from util.walker import FileWalker

class Evaluator(Process):
    def __init__(self, config: Config, client: LlamaClient, docs:List[Document]=[]) -> None:
        super().__init__()
        self.config = config
        self.client = client
        self.docs = docs

    def run(self, args: Any = None):
        if len(self.docs) == 0:
            files = FileWalker(self.config, ".").walk()
            for file in files:
                self.docs.append(self.client.generate_doc(file))
        
        data_gen = DatasetGenerator.from_documents(self.docs, show_progress=self.config.index_params.verbose)
        evals = data_gen.generate_dataset_from_nodes()
        self._run_evals(evals)

    def _run_evals(self, evals):
        llm = OpenAI(model=self.config.llm_params.model_type.value[1], temperature=self.config.temperature, max_tokens=self.config.max_tokens)
        service_context = ServiceContext.from_defaults(llm=llm)
        index = VectorStoreIndex.from_documents(self.docs, service_context=service_context)
        evaluator = RelevancyEvaluator(service_context=service_context)
        qe = index.as_query_engine()
        response = qe.query(evals[0])
        evaluation = evaluator.evaluate_response(query=evals[0], response=response)
        print(evaluation.__dict__)


        
