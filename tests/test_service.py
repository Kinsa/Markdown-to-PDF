"""Unit and integration tests for service.py"""

from io import BytesIO
import pytest

from contextlib import contextmanager
from flask import get_flashed_messages, template_rendered
from service import allowed_file, app as flask_app


@pytest.fixture
def app():
    flask_app.config["TESTING"] = True
    yield flask_app


@pytest.fixture
def client(app):
    return app.test_client()


@contextmanager
def captured_templates(app):
    """Capture templates rendered and their context"""
    recorded = []

    def record(sender, template, context, **extra):
        recorded.append((template, context))

    template_rendered.connect(record, app)
    try:
        yield recorded
    finally:
        template_rendered.disconnect(record, app)


class TestAppConfiguration:
    """Test Flask app configuration"""
    
    def test_app_has_upload_folder_configured(self, app):
        """Test that UPLOAD_FOLDER is configured"""
        assert 'UPLOAD_FOLDER' in app.config
        assert app.config['UPLOAD_FOLDER'] == 'uploads'
    
    def test_app_has_secret_key(self, app):
        """Test that SECRET_KEY is set"""
        assert 'SECRET_KEY' in app.config
        assert app.config['SECRET_KEY'] is not None
    
    def test_upload_directory_exists(self, app):
        """Test that upload directory is created"""
        from pathlib import Path
        upload_dir = Path(app.config['UPLOAD_DIR'])
        assert upload_dir.exists()
        assert upload_dir.is_dir()


class TestAllowedFile:
    """Tests for the allowed_file function"""

    @pytest.mark.unit
    def test_allowed_file(self):
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


class TestSuccessfulFileUpload:
    """Successful upload tests"""

    @pytest.mark.integration
    def test_file_upload_successful_flash(self, client):
        """Test that a markdown file upload results in a successful flash message."""
        with client:
            data = {"file": (BytesIO(b"content"), "test.md")}
            client.post("/", data=data, content_type="multipart/form-data")

            messages = get_flashed_messages()
            assert "Your file has been converted successfully!" in messages


    @pytest.mark.integration
    def test_markdown_conversion_renders_template(self, client, app):
        """Test that index.jinja is rendered with download_url in context"""

        with captured_templates(app) as templates:
            data = {"file": (BytesIO(b"content"), "test.md")}
            response = client.post("/", data=data, content_type="multipart/form-data")

            # Check we got a successful response
            assert response.status_code == 200

            # Check the template and context
            assert len(templates) == 1
            template, context = templates[0]

            assert template.name == "index.jinja"
            assert "download_url" in context
            assert context["title"] == "Markdown to PDF Converter"
            assert context["download_url"] is not None


    @pytest.mark.integration
    def test_download_file(self, client):
        """Test the download_file route serves the file correctly after upload"""

        data = {"file": (BytesIO(b"content"), "test.md")}
        client.post("/", data=data, content_type="multipart/form-data")
        response = client.get("/uploads/test.pdf")

        # Check we got a successful response
        assert response.status_code == 200



class TestEmptyFileUpload:
    """Tests for empty file upload behavior"""
    
    @pytest.mark.integration
    def test_file_type_error_invalid_file_type_flash_and_redirect(self, client):
        """Test that a txt file upload results in an error flash message and a redirect."""
        with client:
            data = {"file": (BytesIO(b"content"), "test.txt")}
            response = client.post("/", data=data, content_type="multipart/form-data")

            # Check we got a redirect response
            assert response.status_code == 302

            messages = get_flashed_messages()
            assert "Invalid file type. Please upload a Markdown file." in messages


    @pytest.mark.integration
    def test_file_type_error_renders_template_without_download_url_context(self, client, app):
        """Test that index.jinja is rendered without download_url in context when there is a file type error"""

        with captured_templates(app) as templates:
            data = {"file": (BytesIO(b"content"), "test.txt")}
            response = client.post(
                "/", data=data, content_type="multipart/form-data", follow_redirects=True
            )

            # Check we got a success response after redirecting
            assert response.status_code == 200

            # Check the template and context
            assert len(templates) == 1
            template, context = templates[0]

            assert template.name == "index.jinja"
            assert "download_url" not in context
            assert context["title"] == "Markdown to PDF Converter"


class TestMissingFileUpload:
    """Tests for missing file upload behavior"""

    @pytest.mark.integration
    def test_missing_file_error_invalid_file_type_flash_and_redirect(self, client):
        """Test that posting without a file results in an error flash message and a redirect."""
        with client:
            response = client.post("/", content_type="multipart/form-data")

            # Check we got a redirect response
            assert response.status_code == 302

            messages = get_flashed_messages()
            assert "You must upload a file." in messages

    @pytest.mark.integration
    def test_missing_file_error_renders_template_without_download_url_context(self, client, app):
        """Test that index.jinja is rendered without download_url in context when posting without a file"""

        with captured_templates(app) as templates:
            response = client.post(
                "/", content_type="multipart/form-data", follow_redirects=True
            )

            # Check we got a success response after redirecting
            assert response.status_code == 200

            # Check the template and context
            assert len(templates) == 1
            template, context = templates[0]

            assert template.name == "index.jinja"
            assert "download_url" not in context
            assert context["title"] == "Markdown to PDF Converter"


class TestEmptyFileSubmission:
    """Tests for empty file submission behavior"""

    @pytest.mark.integration
    def test_empty_file_error_invalid_file_type_flash_and_redirect(self, client):
        """Test that posting empty file results in an error flash message and a redirect."""
        with client:
            data = {"file": (BytesIO(b"content"), "")}
            response = client.post("/", data=data, content_type="multipart/form-data")

            # Check we got a redirect response
            assert response.status_code == 302

            messages = get_flashed_messages()
            assert "You must upload a file." in messages

    @pytest.mark.integration
    def test_empty_file_error_renders_template_without_download_url_context(self, client, app):
        """Test that index.jinja is rendered without download_url in context when posting with an empty file"""

        with captured_templates(app) as templates:
            data = {"file": (BytesIO(b"content"), "")}
            response = client.post(
                "/", data=data, content_type="multipart/form-data", follow_redirects=True
            )

            # Check we got a success response after redirecting
            assert response.status_code == 200

            # Check the template and context
            assert len(templates) == 1
            template, context = templates[0]

            assert template.name == "index.jinja"
            assert "download_url" not in context
            assert context["title"] == "Markdown to PDF Converter"
