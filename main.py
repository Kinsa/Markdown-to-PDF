import sys
import os
import tempfile
from pathlib import Path
from xhtml2pdf import pisa
from markdown import markdownFromFile


def convert_markdown_to_pdf(markdown_file_path):
    """Convert a Markdown file to PDF with the same base name."""
    markdown_path = Path(markdown_file_path)

    if not markdown_path.exists():
        raise FileNotFoundError(f"Markdown file not found: {markdown_file_path}")

    if markdown_path.suffix.lower() not in [".md", ".markdown"]:
        raise ValueError(
            f"File must have .md or .markdown extension: {markdown_file_path}"
        )

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

    html_top_content = """
    <html>
        <head>
            <style>
                @page {
                    size: A4 portrait;
                    margin: 1.6cm 1.2cm 1.2cm;
                }
                
                body {
                    font-size: 13pt;
                    line-height: 1.4;
                }
                
                h1 {
                    font-size: 21pt;
                }
                
                h1, h2, h3, li {
                    margin-bottom: 0;
                    padding-bottom: 0;
                }
                
                h1 + p,
                h2 + h3 {
                    margin-top: 0;
                }
                
                h3 + p {
                    margin-bottom: 0;
                }

                p + p {
                    margin-top: 13pt;
                }

                ul + p {
                    margin-bottom: 0;
                }
                
                ul {
                    margin-bottom: 13pt;
                }
            </style>
        </head>
        <body>
    """

    html_bottom_content = """
        </body>
    </html>
    """

    html_content = "".join(
        [
            html_top_content,
            html_body_content,
            html_bottom_content,
        ]
    )

    # Generate PDF
    try:
        pdf_path = markdown_path.with_suffix(".pdf")
        with open(pdf_path, "wb") as result_file:
            pisa_status = pisa.CreatePDF(
                html_content, dest=result_file, encoding="UTF-8"
            )

        # Check for errors
        if pisa_status.err:
            print("An error occurred!")
        else:
            print(f"Successfully converted {markdown_path} to {pdf_path}")

        return str(pdf_path)
    finally:
        # Clean up temporary HTML file
        # if os.path.exists(temp_html_path):
        #     os.unlink(temp_html_path)
        pass


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
