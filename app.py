import streamlit as st
import fitz
import plotly.graph_objects as go
from datetime import datetime
from resume_analyzer import analyze_resume

st.set_page_config(page_title="AI Resume Analyzer", page_icon="📄", layout="wide")

st.title("AI-Powered Resume Analyzer")
st.write("Advanced resume analysis using semantic AI, NLP, and candidate-job matching.")

uploaded_file = st.file_uploader("Upload Your Resume (PDF)", type=["pdf"])
job_description = st.text_area("Paste Job Description", height=180)

def extract_text_from_pdf(file):
    document = fitz.open(stream=file.getvalue(), filetype="pdf")
    text = ""
    for page in document:
        text += page.get_text()
    document.close()
    return text

if st.button("🔍 Analyze Resume", type="primary"):
    if uploaded_file is None:
        st.warning("Please upload your resume.")
    elif not job_description.strip():
        st.warning("Please enter a job description.")
    else:
        resume_text = extract_text_from_pdf(uploaded_file)

        if not resume_text.strip():
            st.error("No readable text found in the PDF.")
            st.stop()

        with st.spinner("AI is analyzing your resume..."):
            results = analyze_resume(resume_text, job_description)

        st.divider()
        st.header("AI Resume Analysis Dashboard")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Overall Match Score", f"{results['overall_score']:.1f}%")
            st.progress(results["overall_score"] / 100)

        with col2:
            st.metric("Semantic AI Similarity", f"{results['semantic_score']:.1f}%")
            st.progress(results["semantic_score"] / 100)

        with col3:
            st.metric("Technical Skills Match", f"{results['skills']['score']:.1f}%")
            st.progress(results["skills"]["score"] / 100)

        st.divider()
        st.subheader("Candidate Matching Breakdown")

        categories = ["Semantic AI", "Technical Skills", "Education", "Experience", "Projects", "Job Titles"]
        scores = [
            results["semantic_score"],
            results["skills"]["score"],
            results["education"]["score"],
            results["experience"]["score"],
            results["projects"]["score"],
            results["titles"]["score"]
        ]

        fig = go.Figure(data=[
            go.Bar(
                x=categories,
                y=scores,
                marker_color=["#3b82f6", "#22c55e", "#a855f7", "#f59e0b", "#06b6d4", "#ec4899"],
                text=[f"{score:.1f}%" for score in scores],
                textposition="auto"
            )
        ])

        fig.update_layout(
            title="Candidate-Job Matching Analysis",
            yaxis_title="Match Score (%)",
            yaxis_range=[0, 110],
            template="plotly_dark",
            height=450
        )

        st.plotly_chart(fig, use_container_width=True)

        st.divider()
        st.subheader("Technical Skills Analysis")

        col1, col2 = st.columns(2)

        with col1:
            st.success("Matched Skills")
            for skill in results["skills"]["matched"]:
                st.write(skill)
            if not results["skills"]["matched"]:
                st.write("No matching skills identified.")

        with col2:
            st.error("Missing Skills")
            for skill in results["skills"]["missing"]:
                st.write(skill)
            if not results["skills"]["missing"]:
                st.write("No missing skills identified.")

        st.divider()
        st.subheader("Education Analysis")
        st.write("**Degrees Detected:**", ", ".join(results["education"]["resume_degrees"]) or "None")
        st.write("**Degrees Requested:**", ", ".join(results["education"]["required_degrees"]) or "Not specified")

        st.divider()
        st.subheader("Experience Analysis")
        st.write("**Experience Detected:**", results["experience"]["candidate_years"], "years")
        st.write("**Experience Requested:**", results["experience"]["required_years"], "years")

        st.divider()
        st.subheader("Project Relevance")
        st.metric("Project Relevance Score", f"{results['projects']['score']:.1f}%")
        st.write("Project-related lines detected:", results["projects"]["projects_detected"])

        st.divider()
        st.subheader("Job Title Analysis")
        st.write("**Relevant Titles in Resume:**", ", ".join(results["titles"]["resume_titles"]) or "None")
        st.write("**Job Titles in Description:**", ", ".join(results["titles"]["job_titles"]) or "None")

        st.divider()
        st.subheader("AI Improvement Suggestions")

        if results["suggestions"]:
            for suggestion in results["suggestions"]:
                st.info(suggestion)
        else:
            st.success("No major gaps identified by the current analysis.")

        st.divider()
        st.subheader("Download Analysis Report")

        report = f"""AI RESUME ANALYZER REPORT
Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Overall Match Score: {results['overall_score']:.2f}%
Semantic AI Similarity: {results['semantic_score']:.2f}%
Technical Skills Match: {results['skills']['score']:.2f}%
Education Match: {results['education']['score']:.2f}%
Experience Match: {results['experience']['score']:.2f}%
Project Relevance: {results['projects']['score']:.2f}%
Job Title Match: {results['titles']['score']:.2f}%

Matched Skills:
{', '.join(results['skills']['matched']) or 'None'}

Missing Skills:
{', '.join(results['skills']['missing']) or 'None'}

Improvement Suggestions:
{chr(10).join(results['suggestions']) or 'None'}
"""

        st.download_button(
            "Download AI Analysis Report",
            data=report,
            file_name="AI_Resume_Analysis_Report.txt",
            mime="text/plain"
        )

        st.success("Advanced AI resume analysis completed!")
