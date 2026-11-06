
import streamlit as st

st.set_page_config(
    page_title="Fake Job & Internship Detection",
    page_icon="🔍",
    layout="wide"
)

st.title("🔍 Fake Job & Internship Detection System")

st.write(
    "Detect fake job and internship opportunities "
    "using Machine Learning."
)

st.subheader("Job / Internship Analyzer")

job_description = st.text_area(
    "Paste your Job or Internship Description",
    height=200,
    placeholder="Enter job description here..."
)

if st.button("Analyze Job"):
    if job_description.strip():
        st.info("Job description received successfully!")
    else:
        st.warning("Please enter a job description.")
