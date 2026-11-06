
import streamlit as st
import joblib
import re
from bs4 import BeautifulSoup

st.set_page_config(
    page_title="Fake Job & Internship Detection",
    page_icon="🔍",
    layout="wide"
)

# Load Model
model = joblib.load("fake_job_model.pkl")
tfidf = joblib.load("tfidf_vectorizer.pkl")

# Text Cleaning
def clean_text(text):
    text = BeautifulSoup(text, "html.parser").get_text()
    text = text.lower()
    text = re.sub(r'http\S+|www\S+', '', text)
    text = re.sub(r'[^a-z\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

# Scam Keywords
scam_keywords = [
    "registration fee",
    "pay money",
    "processing fee",
    "no experience required",
    "guaranteed job",
    "earn money fast",
    "work from home",
    "instant income",
    "pay immediately",
    "bank details"
]

def detect_scam_keywords(text):
    text = text.lower()
    return [
        keyword for keyword in scam_keywords
        if keyword in text
    ]

# Website UI
st.title("🔍 Fake Job & Internship Detection System")
st.write("AI-powered job scam detection using Machine Learning.")

st.subheader("Job / Internship Analyzer")

job_description = st.text_area(
    "Paste your Job or Internship Description",
    height=250,
    placeholder="Enter job description here..."
)

if st.button("Analyze Job"):

    if job_description.strip():

        cleaned = clean_text(job_description)

        vectorized = tfidf.transform([cleaned])

        prediction = model.predict(vectorized)[0]

        probability = model.predict_proba(vectorized)[0][1]

        st.subheader("📊 Detection Result")

        if prediction == 1:
            st.error("⚠️ Potential Fake Job Detected!")
        else:
            st.success("✅ Likely Genuine Job")

        st.metric(
            "Estimated Fraud Risk",
            f"{probability * 100:.2f}%"
        )

        # Scam Keyword Analysis
        st.subheader("🚨 Scam Keyword Analysis")

        found_keywords = detect_scam_keywords(job_description)

        if found_keywords:
            st.warning("Suspicious keywords detected!")

            for keyword in found_keywords:
                st.write("⚠️", keyword)
        else:
            st.success("No listed scam keywords detected.")

        st.caption(
            "This result is an ML-based estimate, not a guarantee. "
            "Always verify the employer independently."
        )

    else:
        st.warning("Please enter a job description.")
