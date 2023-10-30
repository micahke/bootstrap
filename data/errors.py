NO_CONFIG_FOUND = "No config found. Please create a boot.yaml file and try again."

NO_PROJECT_NAME = "No project name has been set. Please set the `project` value in your bootstrap file"

NO_API_KEY = "No OpenAI API key located. Please set `OPENAI_API_KEY in your path or run 'bootstrap --key YOUR_KEY' to do this for you."

NO_QUERY_PROVIDED = "There was no query provided, please try again."

def __non_boolean(field: str) -> str:
    return f"Non boolean value set for field '{field}'"

NON_BOOLEAN = __non_boolean

def __invalid_value(field: str) -> str:
    return f"Invalid value for field '{field}"

INVALID_VALUE = __invalid_value
