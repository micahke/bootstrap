import yaml
from data.config import Config, IndexType, ModelType
from data.errors import INVALID_VALUE, NO_PROJECT_NAME, NON_BOOLEAN


def parse_config_file(src: str) -> Config:
    data = yaml.safe_load(src)
    config = Config() 
    if "project" not in data:
        print(NO_PROJECT_NAME)
        # TODO: Thing about this. Seems lazy
        exit(0)
    
    config.set_name(data["project"])

    if "description" in data:
        config.set_description(data["description"])

    if "filetypes" in data:
        config.set_filetypes(data['filetypes'])

    if "excluded_dirs" in data:
        config.set_excluded_dirs(data['excluded_dirs'])

    if "llm" in data:
        llm_data = data['llm']
        if "model" in llm_data:
            model_type = llm_data['model']
            if model_type == ModelType.GPT3.value[0]:
                config.set_model_type(ModelType.GPT3)
            elif model_type == ModelType.GPT4.value[0]:
                config.set_model_type(ModelType.GPT4)
            else:
                print(INVALID_VALUE("llm.model"))

    if "index" in data:
        indexData = data['index']
        if "type" in indexData:
            typ = indexData["type"].lower()
            if typ == 'vector':
                config.set_index_type(IndexType.VECTOR)
            if typ == 'tree':
                config.set_index_type(IndexType.TREE)
        if "verbose" in indexData:
            verbose = indexData['verbose']
            # Check if verbose if a boolean
            if type(verbose) == bool:
                config.set_verbose(verbose)
            else:
                print(NON_BOOLEAN("index.verbose"))


    return config
