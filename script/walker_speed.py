import os

from util.parsers import parse_config_file


def run():
    dirname = os.path.dirname(__file__)
    filepath = os.path.join("../boot.yaml")
    config = parse_config_file(filepath)
    print(config)

if __name__ == "__main__":
    run()
