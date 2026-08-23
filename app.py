# FLASK APP
import os
import sys
import json

from flask import Flask, request, render_template
from pypdf import PdfReader

from resumeparser import ats_extractor
from ats_analyzer import calculate_ats_score


sys.path.insert(0, os.path.abspath(os.getcwd()))


UPLOAD_PATH = r"__DATA__"

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route("/process", methods=["POST"])
def ats():

    # -----------------------------
    # 1. Get uploaded resume
    # -----------------------------
    doc = request.files.get('pdf_doc')

    if not doc:
        return render_template(
            'index.html',
            error="Please upload a PDF resume."
        )

    # -----------------------------
    # 2. Get Job Description
    # -----------------------------
    job_description = request.form.get(
        "job_description",
        ""
    ).strip()

    if not job_description:
        return render_template(
            'index.html',
            error="Please enter a Job Description."
        )

    # -----------------------------
    # 3. Save PDF
    # -----------------------------
    os.makedirs(UPLOAD_PATH, exist_ok=True)

    doc_path = os.path.join(
        UPLOAD_PATH,
        "file.pdf"
    )

    doc.save(doc_path)

    # -----------------------------
    # 4. Extract text from PDF
    # -----------------------------
    resume_text = _read_file_from_path(
        doc_path
    )

    # -----------------------------
    # 5. Ollama Resume Parser
    # -----------------------------
    parsed_data = ats_extractor(
        resume_text
    )

    # Convert JSON string → Python dictionary
    try:
        resume_data = json.loads(parsed_data)

    except json.JSONDecodeError:

        resume_data = {
            "raw_response": parsed_data
        }

    # -----------------------------
    # 6. ATS Analyzer
    # -----------------------------
    ats_result = calculate_ats_score(
        resume_text,
        job_description
    )

    # -----------------------------
    # 7. Send everything to HTML
    # -----------------------------
    return render_template(
        'index.html',
        data=resume_data,
        ats_result=ats_result,
        job_description=job_description
    )


def _read_file_from_path(path):

    reader = PdfReader(path)

    data = ""

    for page_no in range(len(reader.pages)):

        page = reader.pages[page_no]

        text = page.extract_text()

        if text:
            data += text + "\n"

    return data


if __name__ == "__main__":

    app.run(
        port=8000,
        debug=True
    )