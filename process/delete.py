from typing import Any
from process.process import Process
from util.fs import delete_bootstrap_dir


class DeleteProcess(Process):
    def __init__(self) -> None:
        super().__init__()

    def run(self, args: Any = None):
        delete_bootstrap_dir()
