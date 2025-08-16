# Markdown To PDF

A Python script to be run from the command line to convert a Markdown document to PDF using fpdf2 and Mistletoe.

## First Time Getting Set Up

[Install UV](https://docs.astral.sh/uv/getting-started/installation/):

```sh
$ curl -LsSf https://astral.sh/uv/install.sh | sh
```

Source the `~/.zshrc` file for changes to take effect:

```sh
$ source ~/.zshrc
```

[Use UV to install the latest Python just for it's use](https://docs.astral.sh/uv/guides/install-python/). Use the latest LTS release.

```sh
$ uv python install
```

### Create a new uv project

```sh
$ uv init .
```

### Create and activate a virtual environment

```sh
$ uv venv .venv
$ source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### Install packages manually the first time

- [fpdf2 Installation Docs](https://py-pdf.github.io/fpdf2/index.html#installation)
- [Installing and using Mistletoe to convert Markdown files to PDF](https://py-pdf.github.io/fpdf2/CombineWithMarkdown.html)
- [Pytest how-to guides](https://docs.pytest.org/en/stable/how-to/index.html)
- [Getting started with Ruff](https://docs.astral.sh/ruff/tutorial/#getting-started)
- [The Black code style](https://black.readthedocs.io/en/stable/the_black_code_style/index.html)

```sh
$ uv add fpdf2 mistletoe 
$ uv add --dev pytest ruff black
$ uv sync
```

## Subsequent Setup

Install UV from the steps in the First Time Getting Set Up section if uv is not installed

Install a suitable Python (pick one that satisfies requires-python in the `pyproject.toml` file)

```sh
$ uv python install 3.13
```

Create a virtual environment (optional; uv sync will create one if missing):

```sh
$ uv venv .venv
```

Install exactly what’s in uv.lock including the dev tools group

```sh
$ uv sync --frozen --all-groups
```

## Editing

### venv activation

Activate the virtual environment to run pytest, black, or ruff directly

```sh
$ source .venv/bin/activate
```

Deactivate the virtual environment

```sh
$ deactivate
```

### uv run

Use `uv run` to run tools without activating the virtual environment, for example:

```sh
$ uv run pytest
```

### Running Tests

```sh
$ pytest test_main.py -v
```

### Code Quality Tools

Always run formatting and linting after making edits:

#### Format code with black

```sh
black main.py
```

#### Check and fix linting issues with ruff

```sh
ruff check --fix main.py
```

#### Verify all checks pass

```sh
ruff check main.py
```

## Configure PyCharm 

[Configure PyCharm to use the uv environment](https://www.jetbrains.com/help/pycharm/uv.html)

### Running Tests in PyCharm

Set pytest as the default test runner:
    
- On macOS: PyCharm > Settings (or Preferences) > Tools > Python Integrated Tools > Testing > Default test runner: pytest.

Create a Run/Debug configuration using pytest:

- Create a new configuration of type “Python tests” > “pytest”.
- Ensure the Working directory is your project root and the Interpreter is your project’s .venv Python.
