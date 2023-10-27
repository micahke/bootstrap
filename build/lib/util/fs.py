import os
import shutil

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
        return True
    return False

def create_bootstrap_dir():
    rootdir = os.getcwd()
    path = os.path.join(rootdir, ".boot")
    os.mkdir(path)
    os.mkdir(os.path.join(path, "storage"))

def get_bootstrap_dir():
    rootdir = os.getcwd()
    return os.path.join(rootdir, ".boot")


def delete_bootstrap_dir():
    dir = get_bootstrap_dir()
    shutil.rmtree(dir)


def get_snapshot_filepath() -> str:
    return os.path.join(get_bootstrap_dir(), "snapshot")

def snapshot_exists() -> bool:
    return os.path.exists(get_snapshot_filepath())
