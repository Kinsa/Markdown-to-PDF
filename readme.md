# Markdown To PDF

Convert a Markdown document to PDF in Python using xhtml2pdf and readme.

## Running 

### Prerequisite Installation

1. Install uv [following the directions](https://docs.astral.sh/uv/getting-started/installation/) if necessary.
2. Install Python (if not already available): `uv python install`
   - This ensures a compatible Python version (>=3.13) is available
3. Sync dependencies: `uv sync --frozen --all-groups`
4. Install the project in editable mode: `uv pip install -e .`
   - This allows tests to import `main` and `service` modules without path manipulation
   - Changes to code are immediately reflected without reinstallation

### Running the Script from the Command Line

Once the prerequisites are installed, run the `main.py` script passing the path to the markdown file as an argument:

```shell
# sh
uv run python main.py spam.md
```

Optionally, specify a CSS file with the `--css` flag:

```shell
# sh
uv run python main.py spam.md --css=eggs.css
```

For more information on defining things such as page size and margins, see the [xhtml2pdf documentation on Defining Page Layouts](https://xhtml2pdf.readthedocs.io/en/latest/format_html.html#pages).

### Running the Web Microservice

```shell
# sh
uv run python fservice.py
```

The service runs in debug mode by default and will be available at http://127.0.0.1:5000

## Release Outline

- [x] Prototype in Code: Python script which takes a markdown file as an argument and returns a formatted PDF
- [x] Styling with CSS: Modify the stying of the output. Building towards having a default stylesheet, the ability to specify a separate stylesheet as a script argument, and documentation for creating additional stylesheets.
- [-] Backend Service: Abstract the functional prototype from the command line interface, adding a web server to allow posting a markdown file and optionally a stylesheet (ref. https://flask.palletsprojects.com/en/stable/patterns/fileuploads/)
    - [-] Test services.py (ref. https://testdriven.io/blog/flask-pytest/)
    - [ ] Delete uploads after processing
    - [ ] Style the tempalate
    - [ ] Allow drag-and-drop uploading (ref. https://developer.mozilla.org/en-US/docs/Web/API/HTML_Drag_and_Drop_API/File_drag_and_drop)
    - [ ] Allow for choosing between stylesheets (currently `default.css` which is a sans-serif typeface and `minimal.css` which just sets up an A4 page size)
- [ ] Mac OS / iOS app: Abstract backend service to use pywebview (JavaScript calls Python directly without web server) / evaluate Tauri (continue to use web server), package into a windowed .app including the frontend build as app data 
- [ ] Allow greater control over styling - one idea would be to choose options e.g. "A4" or "Letter" and "Landscape" or "Portrait" and maybe font, base font size, etc. and have the option to remember that for next time

## Development

### Contributing

By submitting a pull request, you agree that your contributions will be licensed under the same license as this project (MIT), and you grant the project owner (you) perpetual rights to use your contribution in the commercial app.

### Editing

#### venv activation

Activate the virtual environment to run pytest or ruff directly

```shell
# sh
source .venv/bin/activate # On Windows: .venv\Scripts\activate
```

Deactivate the virtual environment

```shell
# sh
deactivate
```

#### uv run

Use `uv run` to run tools without activating the virtual environment, for example:

```shell
# sh
uv run pytest
```

### Running Tests

```shell
# sh
pytest test_main.py -v
```

To run tests and create HTML code coverage reports of the main and service files run (In VSCode use the `ms-vscode.live-server` extension to open these reports in VSCode via the Show Preview option when right-clicking the file):

```shell
# sh 
uv run pytest --cov=main --cov=service --cov-report=html
```

### Code Quality Tools

Always run formatting and linting after making edits:

#### Format code with ruff

```shell
# sh
ruff format main.py
```

#### Check and fix linting issues with ruff

```shell
# sh
ruff check --fix main.py
```

#### Verify all checks pass

```shell
# sh
ruff check main.py
```

### IDE Config

#### Configure PyCharm for Development

- [Configure PyCharm to use the uv environment](https://www.jetbrains.com/help/pycharm/uv.html)
- [Configure PyCharm to Format Code with Black when running the format code command and/or on save](https://www.jetbrains.com/help/pycharm/reformat-and-rearrange-code.html#configure-black)

##### Running Tests in PyCharm

Set pytest as the default test runner:
    
- On macOS: PyCharm > Settings (or Preferences) > Tools > Python Integrated Tools > Testing > Default test runner: pytest.

Create a Run/Debug configuration using pytest:

- Create a new configuration of type “Python tests” > “pytest”.
- Ensure the Working directory is your project root and the Interpreter is your project’s .venv Python.
