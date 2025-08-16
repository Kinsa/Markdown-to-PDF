import pytest
import sys
import tempfile
import os
from unittest.mock import patch
from main import convert_markdown_to_pdf


def test_file_not_found_error():
    """Test that convert_markdown_to_pdf raises FileNotFoundError for non-existent file."""
    non_existent_file = "this_file_does_not_exist.md"
    
    with pytest.raises(FileNotFoundError, match="Markdown file not found"):
        convert_markdown_to_pdf(non_existent_file)


def test_value_error():
    """Test that convert_markdown_to_pdf raises ValueError for file with wrong extension."""
    # Create a temporary file with wrong extension
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as temp_file:
        temp_file.write("Some content")
        temp_file_path = temp_file.name
    
    try:
        with pytest.raises(ValueError, match="File must have .md or .markdown extension"):
            convert_markdown_to_pdf(temp_file_path)
    finally:
        # Clean up the temporary file
        os.unlink(temp_file_path)


def test_main_entry_point():
    """Test that main function prints usage instructions when called without arguments."""
    from main import main

    with pytest.raises(SystemExit) as exc_info:
        main()

    # Verify it exits with error code 1
    assert exc_info.value.code == 1


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
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as temp_file:
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