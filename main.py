import sys
import os
import tempfile
from pathlib import Path
from fpdf import FPDF
from mistletoe import markdown


def convert_markdown_to_pdf(markdown_file_path):
    """Convert a Markdown file to PDF with the same base name."""
    markdown_path = Path(markdown_file_path)

    if not markdown_path.exists():
        raise FileNotFoundError(f"Markdown file not found: {markdown_file_path}")

    if markdown_path.suffix.lower() not in [".md", ".markdown"]:
        raise ValueError(
            f"File must have .md or .markdown extension: {markdown_file_path}"
        )

    # Read markdown content
    with open(markdown_path, "r", encoding="utf-8") as f:
        markdown_content = f.read()

    # Convert markdown to HTML
    html_content = markdown(markdown_content)

    # Create temporary HTML file for processing
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".html", delete=False, encoding="utf-8"
    ) as temp_html:
        temp_html.write(html_content)
        temp_html_path = temp_html.name

    try:
        # Generate PDF
        pdf = FPDF()
        pdf.add_page()
        pdf.write_html(html_content)

        # Create output PDF path with same base name
        pdf_path = markdown_path.with_suffix(".pdf")
        pdf.output(str(pdf_path))

        print(f"Successfully converted {markdown_path} to {pdf_path}")
        return str(pdf_path)

    finally:
        # Clean up temporary HTML file
        if os.path.exists(temp_html_path):
            os.unlink(temp_html_path)


def main():
    """Main entry point for the script."""
    if len(sys.argv) != 2:
        print("Usage: python main.py <markdown_file>")
        sys.exit(1)

    markdown_file = sys.argv[1]

    try:
        convert_markdown_to_pdf(markdown_file)
    except (FileNotFoundError, ValueError) as e:
        print(f"Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
