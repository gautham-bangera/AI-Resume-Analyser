import streamlit as st
import os
from utils.parser import extract_text
from utils.analyzer import extract_skills, match_jobs

# ------------------ PAGE CONFIG ------------------
st.set_page_config(page_title="AI Resume Analyzer", layout="centered")

# ------------------ LOAD CSS ------------------
def load_css():
    with open("assets/style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

# ------------------ CREATE UPLOAD FOLDER ------------------
if not os.path.exists("uploads"):
    os.makedirs("uploads")

# ------------------ UI ------------------
st.title("📄 AI Resume Analyzer")
st.write("Upload your resume and get skill insights + job recommendations")

uploaded_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])

if uploaded_file:
    file_path = os.path.join("uploads", uploaded_file.name)

    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.success("✅ Resume uploaded successfully!")

    # ------------------ PROCESS ------------------
    text = extract_text(file_path)
    skills = extract_skills(text)
    jobs = match_jobs(skills)

    # ------------------ SKILLS ------------------
    st.subheader("🧠 Extracted Skills")

    if skills:
        for skill in skills:
            st.markdown(f'<span class="skill-box">{skill}</span>', unsafe_allow_html=True)
    else:
        st.warning("No skills found")

    # ------------------ JOBS ------------------
    st.subheader("💼 Recommended Jobs")

    for job in jobs:
        st.markdown(f'<div class="job-box">✔ {job}</div>', unsafe_allow_html=True)

    # ------------------ SCORE ------------------
    st.subheader("📊 Resume Score")

    score = min(len(skills) * 10, 100)
    st.progress(score)

    st.markdown(f'<div class="score">Score: {score}/100</div>', unsafe_allow_html=True)