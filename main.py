from util.fs import config_exists, read_config, bootstrap_dir_exists
from data.errors import NO_CONFIG_FOUND
from util.parsers import parse_config_file
from util.walker import FileWalker
from llm.llama_index import LlamaClient

if __name__ == "__main__":
    if not config_exists():
        print(NO_CONFIG_FOUND)
        exit()

    cfg_src = read_config()
    config = parse_config_file(cfg_src)

    bootstrap_dir_exists()

    # files = FileWalker(config, ".").walk()
    # client = LlamaClient()
    # docs = []
    # for file in files:
    #     docs.append(client.generate_doc(file))
    #
    # nodes = client.parse_nodes(docs)
    # index = client.generate_index_from_nodes(nodes)
    # query = "What are some potential bugs? Find one and fix it"
    # client.query(index, query)



