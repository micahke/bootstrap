import argparse
from process.build import BuildProcess
from process.delete import DeleteProcess
from process.evaluator import Evaluator
from process.generation import GenerationProcess
from process.update import UpdateProcess
from util.fs import config_exists, read_config, bootstrap_dir_exists, create_bootstrap_dir
from data.errors import NO_CONFIG_FOUND, NO_QUERY_PROVIDED
from util.parsers import parse_config_file
from util.walker import FileWalker
from llm.llama_index import LlamaClient

parser = argparse.ArgumentParser(description="Enter your bootstrap command")
subparsers = parser.add_subparsers(dest="command")

build_parser = subparsers.add_parser("build")
build_parser.add_argument("-v", "--verbose", action="store_true")
build_parser.add_argument("-s", "--summary", action="store_true")

update_parser = subparsers.add_parser("update")
delete_parser = subparsers.add_parser("delete")
delete_parser = subparsers.add_parser("eval")

ask_parser = subparsers.add_parser("ask")
ask_parser.add_argument('prompt', nargs="?", default="")


def main():
    args = parser.parse_args()

    if not config_exists():
        print(NO_CONFIG_FOUND)
        exit()
    cfg_src = read_config()
    config = parse_config_file(cfg_src)

    client = LlamaClient()

    if not bootstrap_dir_exists():
        create_bootstrap_dir()

    if args.command == 'build':
        BuildProcess(config, client).run(args)
        exit(0)

    if args.command == 'update':
        UpdateProcess(config, client).run()
        exit(0)

    if args.command == 'delete': 
        DeleteProcess().run()
        exit(0)

    if args.command == 'eval':
        Evaluator(config, client).run(args)

    if args.command == 'ask':
        if args.prompt:
            GenerationProcess(config, client, args.prompt).run()
        else:
            print(NO_QUERY_PROVIDED)



if __name__ == "__main__":
    main()
