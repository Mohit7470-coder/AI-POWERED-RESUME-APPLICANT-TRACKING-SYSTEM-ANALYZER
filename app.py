import os
import json

from flask import Flask, request, render_template
from pypdf import PdfReader

from resumeparser import ats_extractor
from ats_analyzer import calculate_ats_score


UPLOAD_PATH = "__DATA__"

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/process", methods=["POST"])
def process_resume():

    # -----------------------------
    # Check PDF
    # -----------------------------

    if "pdf_doc" not in request.files:
        return render_template(
            "index.html",
            error="Please upload a resume PDF."
        )

    doc = request.files["pdf_doc"]

    if doc.filename == "":
        return render_template(
            "index.html",
            error="Please select a PDF file."
        )

    # -----------------------------
    # Get Job Description
    # -----------------------------

    job_description = request.form.get(
        "job_description",
        ""
    ).strip()

    if not job_description:

        return render_template(
            "index.html",
            error="Please enter a job description."
        )

    # -----------------------------
    # Save Resume
    # -----------------------------

    os.makedirs(UPLOAD_PATH, exist_ok=True)

    doc_path = os.path.join(
        UPLOAD_PATH,
        "file.pdf"
    )

    doc.save(doc_path)

    # -----------------------------
    # Extract PDF Text
    # -----------------------------

    resume_text = _read_file_from_path(
        doc_path
    )

    if not resume_text.strip():

        return render_template(
            "index.html",
            error="Could not extract text from the PDF."
        )

    # -----------------------------
    # ATS KEYWORD ANALYSIS
    # -----------------------------

    ats_result = calculate_ats_score(
        resume_text,
        job_description
    )

    # -----------------------------
    # AI RESUME PARSER
    # -----------------------------

    try:

        parsed_data = ats_extractor(
            resume_text
        )

        try:
            parsed_data = json.loads(
                parsed_data
            )

        except json.JSONDecodeError:

            parsed_data = {
                "ai_resume_data": parsed_data
            }

    except Exception as e:

        parsed_data = {
            "ai_resume_data":
                "AI parser error: " + str(e)
        }

    # -----------------------------
    # Combine Results
    # -----------------------------

    final_data = {}

    final_data.update(
        ats_result
    )

    final_data.update(
        parsed_data
    )

    # -----------------------------
    # Send Result to HTML
    # -----------------------------

    return render_template(
        "index.html",
        data=final_data
    )


def _read_file_from_path(path):

    reader = PdfReader(path)

    data = ""

    for page in reader.pages:

        text = page.extract_text()

        if text:
            data += text + "\n"

    return data


if __name__ == "__main__":

    app.run(
        port=8000,
        debug=True
    )