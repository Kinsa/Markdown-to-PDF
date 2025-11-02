"""End-to-end tests using Playwright for browser automation."""

import pytest
from pathlib import Path
from playwright.sync_api import Page, expect


@pytest.fixture(scope="module")
def test_markdown_file(tmp_path_factory):
    """Create a temporary markdown file for testing."""
    tmp_dir = tmp_path_factory.mktemp("test_data")
    md_file = tmp_dir / "test_upload.md"
    md_file.write_text("# Test Heading\n\nThis is a test markdown file.")
    return md_file


@pytest.mark.e2e
def test_successful_upload_shows_success_message(page: Page, test_markdown_file):
    """Test that uploading a markdown file shows a success message."""
    # Navigate to the application
    page.goto("http://127.0.0.1:5000")

    # Verify we're on the right page
    expect(page.locator("h1")).to_have_text("Markdown to PDF Converter")

    # Upload the markdown file
    page.locator('input[type="file"]').set_input_files(str(test_markdown_file))

    # Submit the form
    page.locator('input[type="submit"]').click()

    # Wait for the success message to appear
    success_heading = page.locator('h2:has-text("Success")')
    expect(success_heading).to_be_visible()

    # Verify the success message content
    success_message = page.locator('.flash-success li')
    expect(success_message).to_contain_text("Your file has been converted successfully!")


@pytest.mark.e2e
def test_download_triggered_after_successful_upload(page: Page, test_markdown_file):
    """Test that the PDF download is triggered automatically after upload."""
    # Navigate to the application
    page.goto("http://127.0.0.1:5000")

    # Set up download listener before triggering the action
    with page.expect_download() as download_info:
        # Upload the markdown file
        page.locator('input[type="file"]').set_input_files(str(test_markdown_file))
        page.locator('input[type="submit"]').click()

        # Wait for download to start (triggered by JavaScript)
        download = download_info.value

    # Verify download details
    assert download.suggested_filename == "test_upload.pdf"

    # Optionally save and verify the download
    download_path = Path("downloads") / download.suggested_filename
    download_path.parent.mkdir(exist_ok=True)
    download.save_as(download_path)

    # Verify the file exists and has content
    assert download_path.exists()
    assert download_path.stat().st_size > 0

    # Clean up
    download_path.unlink()


@pytest.mark.e2e
def test_invalid_file_type_shows_error(page: Page, tmp_path):
    """Test that uploading a non-markdown file shows an error message."""
    # Create a text file
    txt_file = tmp_path / "test.txt"
    txt_file.write_text("This is not markdown")

    # Navigate to the application
    page.goto("http://127.0.0.1:5000")

    # Upload the text file
    page.locator('input[type="file"]').set_input_files(str(txt_file))
    page.locator('input[type="submit"]').click()

    # Wait for the error message to appear
    error_heading = page.locator('h2:has-text("Error")')
    expect(error_heading).to_be_visible()

    # Verify the error message content
    error_message = page.locator('.flash-error li')
    expect(error_message).to_contain_text("Invalid file type. Please upload a Markdown file.")


@pytest.mark.e2e
def test_page_title_updates_on_success(page: Page, test_markdown_file):
    """Test that the page title includes 'Success' after successful upload."""
    # Navigate to the application
    page.goto("http://127.0.0.1:5000")

    # Initial title
    expect(page).to_have_title("Markdown to PDF Converter")

    # Upload and submit
    page.locator('input[type="file"]').set_input_files(str(test_markdown_file))
    page.locator('input[type="submit"]').click()

    # Title should now include "Success"
    expect(page).to_have_title("Success | Markdown to PDF Converter")


@pytest.mark.e2e
def test_page_title_updates_on_error(page: Page, tmp_path):
    """Test that the page title includes 'Error' after failed upload."""
    # Create a text file
    txt_file = tmp_path / "test.txt"
    txt_file.write_text("This is not markdown")

    # Navigate to the application
    page.goto("http://127.0.0.1:5000")

    # Upload and submit
    page.locator('input[type="file"]').set_input_files(str(txt_file))
    page.locator('input[type="submit"]').click()

    # Title should now include "Error"
    expect(page).to_have_title("Error | Markdown to PDF Converter")


@pytest.mark.e2e
def test_form_has_accessibility_attributes(page: Page):
    """Test that the form has proper accessibility attributes."""
    page.goto("http://127.0.0.1:5000")

    # Check file input has proper label
    file_input = page.locator('input[type="file"]')
    expect(file_input).to_have_attribute("id", "file")
    expect(file_input).to_have_attribute("required", "")
    expect(file_input).to_have_attribute("accept", ".md,.markdown")

    # Check label exists and is associated
    label = page.locator('label[for="file"]')
    expect(label).to_have_text("Upload Markdown File:")

    # Check ARIA roles on flash messages if present
    # (This will only pass after upload, so we'll just check the structure exists)
    page.wait_for_selector('input[type="submit"]', state="visible")
