import os
from pathlib import Path
from flask import (
    Flask,
    flash,
    request,
    redirect,
    render_template,
    send_from_directory,
    url_for,
)
from werkzeug.utils import secure_filename

from main import convert_markdown_to_pdf


# Get the directory containing this file and create uploads folder
BASE_DIR = Path(__file__).resolve().parent
UPLOAD_FOLDER = "uploads"
UPLOAD_DIR = BASE_DIR / UPLOAD_FOLDER
UPLOAD_DIR.mkdir(exist_ok=True)  # Create the folder if it doesn't exist

ALLOWED_EXTENSIONS = {"md", "markdown"}

app = Flask(__name__)
app.config["UPLOAD_DIR"] = str(UPLOAD_DIR)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["SECRET_KEY"] = "dev-secret-key-change-in-production"


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        # check if the post request has the file part
        if "file" not in request.files:
            flash("You must upload a file.", "error")
            return redirect(request.url)
        file = request.files["file"]
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == "":
            flash("You must upload a file.", "error")
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config["UPLOAD_DIR"], filename))
            pdf_file = convert_markdown_to_pdf(
                os.path.join(app.config["UPLOAD_DIR"], filename),
                "stylesheets/default.css",  # Default CSS file for first version
            )
            # Extract just the filename from the full path returned by convert_markdown_to_pdf
            pdf_filename = os.path.basename(pdf_file)
            flash("Your file has been converted successfully!", "success")

            # Legacy - inintially had automatic download here but for better UX moved to template and triggered download with JS
            # return redirect(url_for("download_file", name=pdf_filename))
            
            # Pass the download URL to the template to trigger automatic download
            download_url = url_for("download_file", name=pdf_filename)
            return render_template(
                "index.jinja",
                title="Markdown to PDF Converter",
                download_url=download_url,
            )
        else:
            flash("Invalid file type. Please upload a Markdown file.", "error")
            return redirect(request.url)
    return render_template("index.jinja", title="Markdown to PDF Converter")


@app.route("/uploads/<name>")
def download_file(name):
    return send_from_directory(app.config["UPLOAD_FOLDER"], name, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
