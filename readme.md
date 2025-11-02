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
5. Install Playwright browsers for end-to-end testing: `uv run playwright install chromium`
   - Only needed if running Playwright tests
   - Chromium is the fastest/smallest browser for testing

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
uv run python service.py
```

The service runs in debug mode by default and will be available at http://127.0.0.1:5000

## Release Outline

- [x] Prototype in Code: Python script which takes a markdown file as an argument and returns a formatted PDF
- [x] Styling with CSS: Modify the stying of the output. Building towards having a default stylesheet, the ability to specify a separate stylesheet as a script argument, and documentation for creating additional stylesheets.
- [ ] **[IN PROGRESS]** Backend Service: Abstract the functional prototype from the command line interface, adding a web server to allow posting a markdown file and optionally a stylesheet (ref. https://flask.palletsprojects.com/en/stable/patterns/fileuploads/)
    - [x] Test services.py (ref. https://testdriven.io/blog/flask-pytest/)
    - [ ] Delete uploads after processing
    - [ ] Style the tempalate
    - [ ] Allow drag-and-drop uploading (ref. https://developer.mozilla.org/en-US/docs/Web/API/HTML_Drag_and_Drop_API/File_drag_and_drop)
    - [ ] Allow for choosing between stylesheets (currently `default.css` which is a sans-serif typeface and `minimal.css` which just sets up an A4 page size)
    - [ ] Containerize / make production ready
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

Run all tests (see note about needing a server to be running for end-to-end tests if doing this):
```shell
# sh
uv run pytest
```

Run specific test types:
```shell
# sh
# Unit tests only
uv run pytest -m unit

# Integration tests only
uv run pytest -m integration

# Everything except end-to-end tests
uv run pytest -m "not e2e"

# Specific test file
uv run pytest tests/test_main.py -v
```

Run non end-to-end tests with coverage reports:
```shell
# sh
# Generate HTML coverage report
uv run pytest -m "not e2e" --cov=main --cov=service --cov-report=html

# Show coverage in terminal with missing lines
uv run pytest -m "not e2e" --cov=main --cov=service --cov-report=term-missing
```

Note: In VSCode use the `ms-vscode.live-server` extension to open HTML coverage reports via the Show Preview option when right-clicking the `htmlcov/index.html` file.

Run Playwright end-to-end tests (requires `playwright install chromium`):

Important: You need to have the Flask server running first:

Terminal 1: Start the server

```shell
# sh
uv run python service.py
```

Terminal 2: Run the tests

```shell
# sh
# Run all Playwright tests
uv run pytest tests/test_e2e.py

# Run all end-to-end tests
uv run pytest -m e2e

# Run in headed mode (see browser)
uv run pytest tests/test_e2e.py --headed

# Run with slow motion for debugging
uv run pytest tests/test_e2e.py --headed --slowmo 1000
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
