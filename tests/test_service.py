import os
import sys

# Ensure project root (one level up from tests/) is on sys.path so service.py can be imported
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from service import allowed_file


def test_allowed_file():
    """Test the allowed_file function for various filenames."""
    # known allowed extensions
    assert allowed_file("document.md") is True
    assert allowed_file("notes.markdown") is True
    # upper and mixed case extensions
    assert allowed_file("UPPERCASE.MD") is True
    assert allowed_file("MiXeD.CaSe.MaRkDoWn") is True
    # disallowed extensions
    assert allowed_file("readme.txt") is False
    assert allowed_file("image.png") is False
    assert allowed_file("archive.zip") is False
    assert allowed_file("no_extension") is False
    assert allowed_file("wrong.extension.doc") is False
    assert allowed_file(".hiddenfile") is False
    assert allowed_file("document.pdf") is False
    