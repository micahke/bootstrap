from llama_index.llms import OpenAI
from data.config import Config
from llm.llama_index import LlamaClient
from process.process import Process
from typing import Any

class GenerationProcess(Process):
    def __init__(self, config: Config, client: LlamaClient, prompt: str) -> None:
        super().__init__()
        self.config = config
        self.client = client
        self.prompt = prompt


    def run(self, args: Any = None):
        llm = OpenAI(model=self.config.llm_params.model_type.value[1], temperature=self.config.temperature, max_tokens=self.config.max_tokens)
        index = self.client.load_index(llm)
        self.client.query(index, self.prompt)



