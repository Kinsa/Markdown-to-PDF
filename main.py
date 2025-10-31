import argparse
import sys
import tempfile
from pathlib import Path
from xhtml2pdf import pisa
from markdown import markdownFromFile


def convert_markdown_to_pdf(markdown_file_path, css_file_path):
    """Convert a Markdown file to PDF with the same base name."""
    markdown_path = Path(markdown_file_path)
    css_path = Path(css_file_path)

    if not markdown_path.exists():
        raise FileNotFoundError(f"Markdown file not found: {markdown_file_path}")

    if not css_path.exists():
        raise FileNotFoundError(f"CSS file not found: {css_file_path}")

    if markdown_path.suffix.lower() not in [".md", ".markdown"]:
        raise ValueError(
            f"File must have .md or .markdown extension: {markdown_file_path}"
        )

    if css_path.suffix.lower() != ".css":
        raise ValueError(f"File must have .css extension: {css_file_path}")

    # Create temporary HTML file for processing
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".html", delete=False
    ) as temp_file:
        temp_html_path = temp_file.name  # Get the path immediately
        print("Created temporary HTML file:", temp_html_path)

    # Convert markdown to HTML
    markdownFromFile(input=str(markdown_path), output=temp_html_path)

    # Read HTML content
    with open(temp_html_path, "r", encoding="utf-8") as f:
        html_body_content = f.read()

    # Read CSS content
    with open(css_path, "r", encoding="utf-8") as f:
        css_content = f.read()

    html_head_open_content = """
    <html>
        <head>
            <style>
    """

    html_head_close_content = """
            </style>
        </head>
        <body>
    """

    html_body_close_content = """
        </body>
    </html>
    """

    html_content = "".join(
        [
            html_head_open_content,
            css_content,
            html_head_close_content,
            html_body_content,
            html_body_close_content,
        ]
    )

    # Generate PDF
    pdf_path = markdown_path.with_suffix(".pdf")
    with open(pdf_path, "wb") as result_file:
        pisa_status = pisa.CreatePDF(html_content, dest=result_file, encoding="UTF-8")

    # Check for errors
    if pisa_status.err:
        print("An error occurred!")
    else:
        print(f"Successfully converted {markdown_path} to {pdf_path}")

    return str(pdf_path)


def main():
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(description="Convert Markdown to PDF")
    parser.add_argument("markdown_file", help="Path to the markdown file")
    parser.add_argument("--css", help="Path to custom CSS file (optional)")

    args = parser.parse_args()

    markdown_file = args.markdown_file
    css_file = args.css or "main.css"  # Use default if not provided

    try:
        convert_markdown_to_pdf(markdown_file, css_file)
    except (FileNotFoundError, ValueError) as e:
        print(f"Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
