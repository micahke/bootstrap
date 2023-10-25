import os
from typing import Any
from process.process import Process


class KeyProcess(Process):
    def __init__(self, key: str) -> None:
        super().__init__()
        self.key = key

    def run(self):
        os.environ['OPENAI_API_KEY'] = self.key
