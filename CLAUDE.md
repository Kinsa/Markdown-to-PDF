# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a simple Python project that converts Markdown files to PDF using the xhtml2pdf and markdown libraries. The main functionality is contained in a single file (`main.py`) that reads a Markdown file, converts it to HTML using markdown, and then generates a PDF using xhtml2pdf.

## Development Environment Setup

The project uses UV for Python package management and virtual environment handling:

```sh
# Install UV (first time only)
curl -LsSf https://astral.sh/uv/install.sh | sh
source ~/.zshrc

# Install Python via UV
uv python install

# Create and activate virtual environment
uv venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
uv sync --frozen --all-groups

# Install project in editable mode (required for tests to import modules)
uv pip install -e .

# Install Playwright browsers (only needed for end-to-end testing)
uv run playwright install chromium
```

**Important**: The `uv pip install -e .` step installs the project in editable mode, which allows tests to import `main` and `service` modules without sys.path manipulation. This is required for the test suite to work properly.

**Playwright Setup**: The `playwright install chromium` command downloads the Chromium browser for end-to-end testing. This is only needed if you're running Playwright tests.

## Core Dependencies

- **xhtml2pdf**: PDF generation library
- **markdown**: Markdown to HTML converter
- **ruff**: Fast Python linter and code formatter
- **pytest**: Testing framework
- **pytest-cov**: Code coverage reporting for pytest
- **Flask**: Web application framework
- **playwright**: Browser automation for end-to-end testing
- **pytest-playwright**: Pytest integration for Playwright

## Project Structure

- `main.py`: Main conversion script that accepts a markdown file argument and outputs PDF
- `test_main.py`: Test file for the conversion script
- `readme.md`: Project documentation and setup instructions
- `.venv/`: Virtual environment directory (managed by UV)
- `service.py`: Flask microservice file

## Running the Application

You can run the application from the command line either by activating the virtual environment or using `uv run`:

```sh
# Option 1: Activate virtual environment first
source .venv/bin/activate
python main.py <input_file.md>

# Option 2: Use uv run (no activation needed)
uv run python main.py <input_file.md>
```

The command line script (`main.py`) accepts a markdown file as a command-line argument and outputs a PDF with the same base name.

## Running the Web Service

You can run the Flask web service from the command line either by activating the virtual environment or using `uv run`:

```sh
# Option 1: Activate virtual environment first
source .venv/bin/activate
python service.py

# Option 2: Use uv run (no activation needed)
uv run python service.py
```

The service script (`service.py`) starts a web server at http://127.0.0.1:5000 in debug mode by default, which means it will automatically reload when you make code changes.

## Code Quality Tools

Always run formatting and linting after making edits. You can either activate the virtual environment or use `uv run`:

```sh
# Option 1: With activated virtual environment
source .venv/bin/activate
ruff format main.py
ruff check --fix main.py
ruff check main.py

# Option 2: Using uv run (no activation needed)
uv run ruff format main.py
uv run ruff check --fix main.py
uv run ruff check main.py
```

## Testing

Always run tests after making changes. Tests help ensure code quality and catch regressions. You can either activate the virtual environment or use `uv run`:

```sh
# Option 1: With activated virtual environment
source .venv/bin/activate
pytest
pytest -v
pytest tests/test_main.py

# Option 2: Using uv run (no activation needed)
uv run pytest
uv run pytest -v
uv run pytest tests/test_main.py
```

### Test Types and Markers

Tests are organized using pytest markers:
- `@pytest.mark.unit` - Unit tests that test individual functions in isolation
- `@pytest.mark.integration` - Integration tests that test multiple components together

Run specific test types:
```sh
# Run only unit tests
uv run pytest -m unit

# Run only integration tests
uv run pytest -m integration
```

### Coverage Reporting

Generate code coverage reports:
```sh
# HTML report (view in browser)
uv run pytest --cov=main --cov=service --cov-report=html

# Terminal report with missing lines
uv run pytest --cov=main --cov=service --cov-report=term-missing
```

### Playwright End-to-End Tests

Run browser-based end-to-end tests (requires `playwright install chromium`):
```sh
# Run Playwright tests headless
uv run pytest tests/test_e2e.py

# Run with visible browser
uv run pytest tests/test_e2e.py --headed

# Run with slow motion for debugging
uv run pytest tests/test_e2e.py --headed --slowmo 1000
```

When adding new functionality, either specify what tests to write or ask for test suggestions to ensure proper coverage.

## IDE Configuration

The project is configured for PyCharm with UV integration. See the [PyCharm UV documentation](https://www.jetbrains.com/help/pycharm/uv.html) for setup details.