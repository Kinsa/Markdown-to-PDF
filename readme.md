# Markdown To PDF

A Python script to be run from the command line to convert a Markdown document to PDF using xhtml2pdf and readme.

## Running the Script

### Prerequisite Installation

1. Install uv following the directions from the *Development* section if necessary.
2. Install a suitable Python version using uv from the *Subsequent Setup* section.
3. Install the package by running the command: `uv sync --frozen`

### Running the Script

Once the prerequisites are installed, run the `main.py` script passing the path to the markdown file as an argument:

```sh
# sh
uv run main.py spam.md
```

## Release Outline

1. [x] Prototype in Code: Python script which takes a markdown file as an argument and returns a formatted PDF
2. [ ] Styling with CSS: Modify the stying of the output. Building towards having a default stylesheet, the ability to specify a separate stylesheet as a script argument, and documentation for creating additional stylesheets.
3. [ ] Backend Service with REST API: Abstract the functional prototype from the command line interface, adding a web server and REST API to allow posting a markdown file and optionally a stylesheet
4. [ ] Frontend Interface: Design an interface for drag-and-drop/file browser choice of the files
5. [ ] Stylesheet Saving: Allow the saving and basic management (renaming, removal) of stylesheets for future use
6. [ ] Mac OS / iOS app: Abstract backend service to use pywebview (JavaScript calls Python directly without REST API) / evaluate Tauri (continue to use the REST API), package into a windowed .app including the frontend build as app data 

## Development

### First Time Getting Set Up

[Install UV](https://docs.astral.sh/uv/getting-started/installation/):

```sh
# sh
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Source the `~/.zshrc` file for changes to take effect:

```sh
# sh
source ~/.zshrc
```

[Use UV to install the latest Python just for it's use](https://docs.astral.sh/uv/guides/install-python/).

```sh
# sh
uv python install
```

### Create a new uv project

```sh
# sh
uv init .
```

### Install packages manually the first time

- [xhtml2pdf Docs](https://xhtml2pdf.readthedocs.io/en/latest/quickstart.html)
- [markdown documentation](https://python-markdown.github.io/reference/)
- [Pytest how-to guides](https://docs.pytest.org/en/stable/how-to/index.html)
- [Getting started with Ruff](https://docs.astral.sh/ruff/tutorial/#getting-started)
- [The Black code style](https://black.readthedocs.io/en/stable/the_black_code_style/index.html)

```sh
# sh
uv add xhtml2pdf markdown 
uv add --dev pytest ruff black
uv sync
```

### Subsequent Setup

Install uv from the steps in the *First Time Getting Set Up* section if uv is not installed

Install a suitable Python (pick one that satisfies requires-python in the `pyproject.toml` file)

```sh
# sh
uv python install 3.13
```

Create a virtual environment (optional; `uv sync` will create one if missing):

```sh
# sh
uv venv .venv
```

Install exactly what’s in `uv.lock` including the dev tools group

```sh
# sh
uv sync --frozen --all-groups
```

### Editing

#### venv activation

Activate the virtual environment to run pytest, black, or ruff directly

```sh
# sh
source .venv/bin/activate # On Windows: .venv\Scripts\activate
```

Deactivate the virtual environment

```sh
# sh
deactivate
```

#### uv run

Use `uv run` to run tools without activating the virtual environment, for example:

```sh
# sh
uv run pytest
```

### Running Tests

```sh
# sh
pytest test_main.py -v
```

### Code Quality Tools

Always run formatting and linting after making edits:

#### Format code with black

```sh
# sh
black main.py
```

#### Check and fix linting issues with ruff

```sh
# sh
ruff check --fix main.py
```

#### Verify all checks pass

```sh
# sh
ruff check main.py
```

### Configure PyCharm for Development

- [Configure PyCharm to use the uv environment](https://www.jetbrains.com/help/pycharm/uv.html)
- [Configure PyCharm to Format Code with Black when running the format code command and/or on save](https://www.jetbrains.com/help/pycharm/reformat-and-rearrange-code.html#configure-black)

#### Running Tests in PyCharm

Set pytest as the default test runner:
    
- On macOS: PyCharm > Settings (or Preferences) > Tools > Python Integrated Tools > Testing > Default test runner: pytest.

Create a Run/Debug configuration using pytest:

- Create a new configuration of type “Python tests” > “pytest”.
- Ensure the Working directory is your project root and the Interpreter is your project’s .venv Python.
