
import streamlit as st
import joblib
import re
from bs4 import BeautifulSoup

st.set_page_config(
    page_title="Fake Job & Internship Detection",
    page_icon="🔍",
    layout="wide"
)

# Load trained model and vectorizer
model = joblib.load("fake_job_model.pkl")
tfidf = joblib.load("tfidf_vectorizer.pkl")

def clean_text(text):
    text = BeautifulSoup(text, "html.parser").get_text()
    text = text.lower()
    text = re.sub(r'http\S+|www\S+', '', text)
    text = re.sub(r'[^a-z\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

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

        if prediction == 1:
            st.error("⚠️ Potential Fake Job Detected!")
        else:
            st.success("✅ Likely Genuine Job")

        st.metric(
            "Estimated Fraud Risk",
            f"{probability * 100:.2f}%"
        )

        st.caption(
            "This is a machine-learning estimate, not a guarantee. "
            "Always verify the employer independently."
        )

    else:
        st.warning("Please enter a job description.")
