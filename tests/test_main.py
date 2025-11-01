import pytest
import sys
import tempfile
import os

from unittest.mock import patch

# Ensure project root (one level up from tests/) is on sys.path so main.py can be imported
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from main import convert_markdown_to_pdf


def test_markdown_file_not_found_error():
    """Test that convert_markdown_to_pdf raises FileNotFoundError for a non-existent markdown file."""
    non_existent_file = "this_file_does_not_exist.md"

    with pytest.raises(FileNotFoundError, match="Markdown file not found"):
        convert_markdown_to_pdf(non_existent_file, "stylesheets/default.css")


def test_css_file_not_found_error():
    """Test that convert_markdown_to_pdf raises FileNotFoundError for a non-existent CSS file."""
    non_existent_file = "this_file_does_not_exist.css"

    with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as temp_file:
        temp_file.write("Some content")
        temp_file_path = temp_file.name

    try:
        with pytest.raises(FileNotFoundError, match="CSS file not found"):
            convert_markdown_to_pdf(temp_file_path, non_existent_file)
    finally:
        # Clean up the temporary file
        os.unlink(temp_file_path)


def test_markdown_file_extension_value_error():
    """Test that convert_markdown_to_pdf raises ValueError for file with wrong extension."""
    # Create a temporary file with wrong extension
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".txt", delete=False
    ) as temp_file:
        temp_file.write("Some content")
        temp_file_path = temp_file.name

    try:
        with pytest.raises(
            ValueError, match="File must have .md or .markdown extension"
        ):
            convert_markdown_to_pdf(temp_file_path, "stylesheets/default.css")
    finally:
        # Clean up the temporary file
        os.unlink(temp_file_path)


def test_css_file_extension_value_error():
    """Test that convert_markdown_to_pdf raises ValueError for file with wrong extension."""
    # Create a temporary file with wrong extension
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".scss", delete=False
    ) as temp_file:
        temp_file.write("Some content")
        temp_file_path = temp_file.name

    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".md", delete=False
    ) as temp_md_file:
        temp_md_file.write("Some content")
        temp_md_file_path = temp_md_file.name

    try:
        with pytest.raises(ValueError, match="File must have .css extension"):
            convert_markdown_to_pdf(temp_md_file_path, temp_file_path)
    finally:
        # Clean up the temporary file
        os.unlink(temp_file_path)


def test_css_file_is_used():
    """Test that convert_markdown_to_pdf uses the custom CSS file."""
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".md", delete=False
    ) as temp_md_file:
        temp_md_file.write("Some content")
        temp_md_file_path = temp_md_file.name

    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".css", delete=False
    ) as temp_css_file:
        temp_css_file.write("h1 { color: red; }")
        temp_css_file_path = temp_css_file.name

    try:
        # Mock pisa.CreatePDF to capture the HTML content passed to it
        with patch("main.pisa.CreatePDF") as mock_create_pdf:
            # Configure the mock to return a successful status
            mock_create_pdf.return_value.err = False

            convert_markdown_to_pdf(temp_md_file_path, temp_css_file_path)

            # Assert that CreatePDF was called
            mock_create_pdf.assert_called_once()

            # Get the HTML content that was passed to CreatePDF
            call_args = mock_create_pdf.call_args
            html_content = call_args[0][0]  # First positional argument

            # Assert that the custom CSS is included in the HTML
            assert "h1 { color: red; }" in html_content
            assert "<style>" in html_content
            assert "</style>" in html_content

    finally:
        # Clean up temporary files
        os.unlink(temp_md_file_path)
        os.unlink(temp_css_file_path)


def test_main_entry_point():
    """Test that main function prints usage instructions when called without arguments."""
    from main import main

    with pytest.raises(SystemExit) as exc_info:
        main()

    # Verify it exits with error code 2
    assert exc_info.value.code == 2


def test_main_file_not_found_error():
    """Test that main function handles FileNotFoundError and exits with code 1."""
    from main import main

    # Mock sys.argv to simulate command line argument
    with patch.object(sys, "argv", ["main.py", "non_existent_file.md"]):
        with pytest.raises(SystemExit) as exc_info:
            main()

        # Verify it exits with error code 1
        assert exc_info.value.code == 1


def test_main_value_error():
    """Test that main function handles ValueError and exits with code 1."""
    from main import main

    # Create a temporary file with wrong extension
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".txt", delete=False
    ) as temp_file:
        temp_file.write("Some content")
        temp_file_path = temp_file.name

    try:
        # Mock sys.argv to simulate command line argument with wrong file extension
        with patch.object(sys, "argv", ["main.py", temp_file_path]):
            with pytest.raises(SystemExit) as exc_info:
                main()

            # Verify it exits with error code 1
            assert exc_info.value.code == 1
    finally:
        # Clean up the temporary file
        os.unlink(temp_file_path)
