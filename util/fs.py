import os

BOOTSTRAP_FILE_NAME = ".bootstrap"


def read_config() -> str:
    rootdir = os.getcwd()
    filepath = os.path.join(rootdir, BOOTSTRAP_FILE_NAME)
    with open(filepath, 'r') as file:
        return file.read()

def config_exists() -> bool:
    rootdir = os.getcwd()
    filepath = os.path.join(rootdir, BOOTSTRAP_FILE_NAME)
    return os.path.exists(filepath)

def read_file(filepath: str) -> str:
    with open(filepath, 'r') as file:
        return file.read()


def bootstrap_dir_exists() -> bool:
    rootdir = os.getcwd()
    path = os.path.join(rootdir, ".boot")
    if os.path.exists(path):
        print("okay")

    return True
