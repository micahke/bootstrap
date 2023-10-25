# Bootstrap

Bootstrap is a CLI tool that indexes your code project and allows you to make complex queries with the full scope of the project in context. It relies on the [llama-index](https://github.com/run-llama/llama_index) framework. Because this uses OpenAI's GPT models, an OpenAI API key will be required.

## Installation

In order to install Bootstrap, run the following in your terminal. Python must be installed on your machine.

```sh
pip install git+https://github.com/micahke/bootstrap.git
```

## Setup

First, make sure your OpenAI API key is set as an environment variable called `OPENAI_API_KEY`:

```sh
# Mac / Linux
export OPENAI_API_KEY='your-api-key-here'

# Windows
echo "export OPENAI_API_KEY='your-api-key-here'" >> ~/.bash_profile
```

Bootstrap runs in the project directory itself. This means that a config file is required in the root directory of your project called `.bootstrap`. This file is in `yaml` format:

```yaml
project: project_name # Required
description: A small description of your project # Optional

filetypes: [".py", ".md", ".txt"] # Required
excluded_dirs: [".venv", "docs"] # Optional
```

## Usage

> Make sure that

Bootstrap has 3 main commands: `build`, `ask`, and `delete`. In order to build an index from your code, simply run the following:

```sh
bootstrap build
```

This creates an index in the .boot folder of your project. Depending on the size of the project, this may take a few seconds. This will be improved when incremental building is added.

Once built, you can ask a question like this:

```sh
bootstrap ask "How does the event system work in this project?"
```

To delete the index, simply run `bootstrap delete`.

> Make sure to add `.boot` and `.bootstrap` to your `.gitignore` file unless you want to index to be portable.
