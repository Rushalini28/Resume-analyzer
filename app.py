
import streamlit as st
import fitz
import re
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

st.set_page_config(
    page_title="Resume Analyzer",
    page_icon="📄",
    layout="wide"
)

st.title("📄 Resume Analyzer and Job Matcher")
st.write("Analyze your resume and compare it with a job description.")

SKILLS = [
    "python", "java", "c++", "sql", "html", "css",
    "javascript", "react", "flask", "django", "streamlit",
    "machine learning", "deep learning", "data analysis",
    "pandas", "numpy", "scikit-learn", "tensorflow",
    "git", "github", "rest api", "mongodb", "mysql",
    "postgresql", "problem solving", "data structures",
    "algorithms", "communication", "docker", "aws"
]


def extract_resume_text(pdf_file):
    document = fitz.open(stream=pdf_file.read(), filetype="pdf")
    text = "\n".join(page.get_text() for page in document)
    document.close()
    return text


def find_skills(text):
    text = text.lower()
    found = []

    for skill in SKILLS:
        pattern = r"(?<!\w)" + re.escape(skill) + r"(?!\w)"
        if re.search(pattern, text):
            found.append(skill)

    return sorted(found)


def calculate_match(resume, job):
    vectorizer = TfidfVectorizer(stop_words="english")
    vectors = vectorizer.fit_transform([resume, job])
    score = cosine_similarity(vectors[0:1], vectors[1:2])[0][0]
    return round(score * 100, 2)


resume_file = st.file_uploader(
    "Upload your resume (PDF only)",
    type=["pdf"]
)

job_description = st.text_area(
    "Paste the job description",
    height=220,
    placeholder="Paste the complete job description here..."
)

if st.button("Analyze Resume", type="primary"):
    if resume_file is None:
        st.error("Please upload your resume PDF.")
    elif not job_description.strip():
        st.error("Please paste a job description.")
    else:
        try:
            resume_text = extract_resume_text(resume_file)

            if not resume_text.strip():
                st.error(
                    "No text found. Upload a text-based PDF, "
                    "not a scanned image PDF."
                )
            else:
                resume_skills = find_skills(resume_text)
                job_skills = find_skills(job_description)

                matched = [
                    skill for skill in job_skills
                    if skill in resume_skills
                ]
                missing = [
                    skill for skill in job_skills
                    if skill not in resume_skills
                ]

                score = calculate_match(
                    resume_text,
                    job_description
                )

                st.subheader("Analysis Results")

                col1, col2, col3 = st.columns(3)
                col1.metric("Text Similarity", f"{score}%")
                col2.metric("Matched Skills", len(matched))
                col3.metric("Missing Skills", len(missing))

                st.progress(int(score))

                st.caption(
                    "Similarity is a text-based estimate, "
                    "not a guaranteed ATS score or hiring prediction."
                )

                left, right = st.columns(2)

                with left:
                    st.subheader("✅ Matched Skills")
                    if matched:
                        st.write(", ".join(matched))
                    else:
                        st.write("No listed skills matched.")

                with right:
                    st.subheader("📌 Skills to Review")
                    if missing:
                        st.write(", ".join(missing))
                    else:
                        st.write(
                            "All skills in this checklist were found."
                        )

                st.subheader("💡 Suggestions")
                suggestions = []

                if missing:
                    suggestions.append(
                        "Review the missing skills and learn "
                        "or demonstrate the relevant ones."
                    )

                if score < 40:
                    suggestions.append(
                        "Tailor your resume summary and project "
                        "descriptions to your actual relevant experience."
                    )

                if not re.search(
                    r"\b(project|projects)\b",
                    resume_text,
                    re.IGNORECASE
                ):
                    suggestions.append(
                        "Add a Projects section with technologies "
                        "used and your actual contributions."
                    )

                if not re.search(
                    r"\b(internship|experience|employment)\b",
                    resume_text,
                    re.IGNORECASE
                ):
                    suggestions.append(
                        "Include relevant experience or internships "
                        "if you have them."
                    )

                if not suggestions:
                    suggestions.append(
                        "Review your results and ensure your "
                        "skills and project details are accurate."
                    )

                for suggestion in suggestions:
                    st.write("• " + suggestion)

                with st.expander("View extracted resume text"):
                    st.text(resume_text)

                report = pd.DataFrame({
                    "Category": (
                        ["Matched skill"] * len(matched)
                        + ["Skill to review"] * len(missing)
                    ),
                    "Skill": matched + missing
                })

                st.download_button(
                    "Download Skills Report (CSV)",
                    data=report.to_csv(index=False),
                    file_name="resume_analysis.csv",
                    mime="text/csv"
                )

        except Exception as error:
            st.error(f"Could not analyze this PDF: {error}")
