import yaml
from data.config import Config
from data.errors import NO_PROJECT_NAME


def parse_config_file(src: str) -> Config:
    data = yaml.safe_load(src)
    config = Config() 
    if "project" not in data:
        print(NO_PROJECT_NAME)
        return
    
    config.set_name(data["project"])

    if "description" in data:
        config.set_description(data["description"])

    if "filetypes" in data:
        config.set_filetypes(data['filetypes'])

    if "excluded_dirs" in data:
        config.set_excluded_dirs(data['excluded_dirs'])

    return config
