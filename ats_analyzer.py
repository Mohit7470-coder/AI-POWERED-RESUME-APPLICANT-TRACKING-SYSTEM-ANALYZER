import re


def normalize_text(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9+#.\- ]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def extract_keywords(job_description):

    jd = normalize_text(job_description)

    common_skills = [
        "python",
        "java",
        "javascript",
        "typescript",
        "c++",
        "sql",
        "mysql",
        "mongodb",
        "postgresql",
        "html",
        "css",
        "react",
        "node.js",
        "express",
        "flask",
        "django",
        "fastapi",
        "pandas",
        "numpy",
        "scikit-learn",
        "tensorflow",
        "pytorch",
        "machine learning",
        "deep learning",
        "nlp",
        "computer vision",
        "git",
        "github",
        "docker",
        "aws",
        "azure",
        "gcp",
        "linux",
        "rest api",
        "api",
        "streamlit",
        "power bi",
        "tableau",
        "excel"
    ]

    found_keywords = []

    for skill in common_skills:
        if skill in jd:
            found_keywords.append(skill)

    return found_keywords


def calculate_keyword_match(resume_text, job_description):

    resume = normalize_text(resume_text)

    keywords = extract_keywords(job_description)

    if not keywords:
        return {
            "score": 0,
            "matched": [],
            "missing": []
        }

    matched = []
    missing = []

    for keyword in keywords:

        if keyword in resume:
            matched.append(keyword)
        else:
            missing.append(keyword)

    score = round(
        (len(matched) / len(keywords)) * 100
    )

    return {
        "score": score,
        "matched": matched,
        "missing": missing
    }


def check_resume_sections(resume_text):

    resume = normalize_text(resume_text)

    sections = {
        "education": [
            "education",
            "academic"
        ],

        "experience": [
            "experience",
            "employment",
            "work history"
        ],

        "skills": [
            "skills",
            "technical skills"
        ],

        "projects": [
            "projects",
            "project"
        ],

        "certifications": [
            "certification",
            "certifications"
        ]
    }

    found = []
    missing = []

    for section, keywords in sections.items():

        exists = any(
            keyword in resume
            for keyword in keywords
        )

        if exists:
            found.append(section)
        else:
            missing.append(section)

    score = round(
        (len(found) / len(sections)) * 100
    )

    return {
        "score": score,
        "found": found,
        "missing": missing
    }


def calculate_ats_score(resume_text, job_description):

    keyword_result = calculate_keyword_match(
        resume_text,
        job_description
    )

    section_result = check_resume_sections(
        resume_text
    )

    keyword_score = keyword_result["score"]
    section_score = section_result["score"]

    final_score = round(
        (keyword_score * 0.70) +
        (section_score * 0.30)
    )

    return {
        "ats_score": final_score,

        "keyword_match": keyword_score,

        "resume_structure": section_score,

        "matched_keywords":
            keyword_result["matched"],

        "missing_keywords":
            keyword_result["missing"],

        "sections_found":
            section_result["found"],

        "sections_missing":
            section_result["missing"]
    }