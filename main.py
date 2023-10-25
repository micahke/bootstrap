import argparse
from util.fs import config_exists, read_config, bootstrap_dir_exists, create_bootstrap_dir, delete_bootstrap_dir
from data.errors import NO_CONFIG_FOUND
from util.parsers import parse_config_file
from util.walker import FileWalker
from llm.llama_index import LlamaClient

parser = argparse.ArgumentParser(description="Enter your bootstrap command")

parser.add_argument("-b", "--build", action="store_true")
parser.add_argument("-d","--delete", action="store_true")
parser.add_argument("prompt", nargs="?", default="")

def build(client: LlamaClient):
    files = FileWalker(config, ".").walk()
    docs = []
    for file in files:
        docs.append(client.generate_doc(file))

    nodes = client.parse_nodes(docs)
    index = client.generate_index_from_nodes(nodes)
    client.save_index(index)

def handle_prompt(client: LlamaClient, prompt: str):
    index = client.load_index()
    client.query(index, prompt)

def delete():
    delete_bootstrap_dir()

if __name__ == "__main__":
    args = parser.parse_args()

    if not config_exists():
        print(NO_CONFIG_FOUND)
        exit()
    cfg_src = read_config()
    config = parse_config_file(cfg_src)

    client = LlamaClient()

    if not bootstrap_dir_exists():
        create_bootstrap_dir()

    if args.build:
        build(client)
        exit(0)

    if args.delete:
        delete()
        exit(0)

    prompt = args.prompt
    if prompt:
        handle_prompt(client, prompt)
    else:
        print("No query provided")

    # query = "What does this program do?"
    # client.query(index, query)



