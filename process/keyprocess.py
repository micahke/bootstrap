import os
from process.process import Process


class KeyProcess(Process):
    def __init__(self, key: str) -> None:
        super().__init__()
        self.key = key

    def run(self, args: None):
        os.environ['OPENAI_API_KEY'] = self.key
