from dataclasses import dataclass
from enum import Enum
from typing import Literal, Optional, List

class ModelType(Enum):
    GPT3 = ['gpt3', 'gpt-3.5-turbo-16k', 16385]
    GPT4 = ["gpt4", "gpt-4", 8192]
    GPT4T = ['gpt4t', "gpt-4-1106-preview", 128000]


@dataclass
class LLMParams:
    model_type: ModelType

class IndexType(Enum):
    VECTOR =  "vector"
    TREE = "tree"

@dataclass
class ConfigIndexParams:
    index_type: IndexType
    verbose: bool

class Config:
    def __init__(self, name: Optional[str] = "") -> None:
        self.name = name
        self.description = ""
        self.filetypes: List[str] = []
        self.excluded_dirs: List[str] = []
        self.index_params = ConfigIndexParams(index_type=IndexType.VECTOR, verbose=False)
        self.llm_params = LLMParams(model_type=ModelType.GPT3)
        self.temperature = 0.1
        self.max_tokens = None

    def set_name(self, name: str):
        self.name = name

    def set_description(self, description: str):
        self.description = description

    def set_filetypes(self, filetypes: List[str]):
        self.filetypes = filetypes

    def set_excluded_dirs(self, excluded_dirs: List[str]):
        self.excluded_dirs = excluded_dirs

    def set_index_type(self, index_type: IndexType):
        self.index_params.index_type = index_type

    def set_verbose(self, verbose: bool):
        self.index_params.verbose = verbose

    def set_model_type(self, model_type: ModelType):
        self.llm_params.model_type = model_type

    def set_temperature(self, temp: int):
        self.temperature = temp

    def set_max_tokens(self, tokens: int):
        self.max_tokens = tokens
