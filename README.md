# Resume Analyzer and Job Matcher

## Description
A Python-based web application that analyzes PDF resumes and compares them with job descriptions. It estimates text similarity, identifies matching and missing skills, provides resume improvement suggestions, and exports a skills report.

## Features
- PDF resume text extraction
- Job description comparison
- TF-IDF and cosine similarity
- Matched and missing skill identification
- Resume improvement suggestions
- CSV report download

## Technologies
- Python
- Streamlit
- PyMuPDF
- Scikit-learn
- Pandas

## Installation

1. Clone or download the repository.
2. Create a virtual environment:
   `py -m venv .venv`
3. Activate it on Windows:
   `.\.venv\Scripts\Activate.ps1`
4. Install dependencies:
   `python -m pip install -r requirements.txt`
5. Run the application:
   `python -m streamlit run app.py`

## Limitations
The similarity score is an estimate of text overlap, not an official ATS score. Skill detection uses a predefined list and does not establish whether a candidate is qualified for a role.
