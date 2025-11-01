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
uv add xhtml2pdf markdown
uv add --dev pytest ruff
uv sync
```

## Core Dependencies

- **xhtml2pdf**: PDF generation library
- **markdown**: Markdown to HTML converter
- **ruff**: Fast Python linter and code formatter
- **pytest**: Testing framework
- **Flask**: Web application framework

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
pytest test_main.py

# Option 2: Using uv run (no activation needed)
uv run pytest
uv run pytest -v
uv run pytest test_main.py
```

When adding new functionality, either specify what tests to write or ask for test suggestions to ensure proper coverage.

## IDE Configuration

The project is configured for PyCharm with UV integration. See the [PyCharm UV documentation](https://www.jetbrains.com/help/pycharm/uv.html) for setup details.