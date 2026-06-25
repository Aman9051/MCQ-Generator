import os
import json
import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from langchain_community.callbacks.manager import get_openai_callback

from mcqgenerator.utils import read_file, get_table_data
from mcqgenerator.MCQgenerator import generate_evaluate_chain
from mcqgenerator.logger import get_logger

load_dotenv()
logger = get_logger(__name__)

with open("Response.json", "r") as f:
    RESPONSE_JSON = json.load(f)

st.set_page_config(page_title="MCQ Generator", page_icon="🦜", layout="centered")
st.title("🦜⛓️ MCQ Generator App")
st.markdown("Generate Multiple Choice Questions from any PDF or TXT file using AI.")

with st.sidebar:
    st.header("⚙️ How it works")
    st.markdown("""
1. Upload a PDF or TXT file
2. Set number of MCQs, subject & difficulty
3. Click **Generate MCQs**
4. Review questions and AI feedback
""")

with st.form("user_inputs"):
    uploaded_file = st.file_uploader("📄 Upload PDF or TXT file", type=["pdf", "txt"])

    col1, col2, col3 = st.columns(3)
    with col1:
        mcq_count = st.number_input("Number of MCQs", min_value=1, max_value=20, value=5)
    with col2:
        subject = st.text_input("Subject", placeholder="e.g. Biology")
    with col3:
        tone = st.selectbox("Difficulty", options=["simple", "medium", "hard"])

    submit = st.form_submit_button("🚀 Generate MCQs", use_container_width=True)

if submit:
    if uploaded_file is None:
        st.error("⚠️ Please upload a PDF or TXT file.")
        st.stop()
    if not subject.strip():
        st.error("⚠️ Please enter a subject.")
        st.stop()

    with st.spinner("⏳ Generating MCQs with AI..."):
        try:
            text = read_file(uploaded_file)
            if not text.strip():
                st.error("⚠️ The file appears empty or unreadable.")
                st.stop()

            with get_openai_callback() as cb:
                response = generate_evaluate_chain({
                    "text":          text,
                    "number":        mcq_count,
                    "subject":       subject,
                    "tone":          tone,
                    "response_json": json.dumps(RESPONSE_JSON)
                })

            quiz   = response.get("quiz", "")
            review = response.get("review", "")

            st.success("✅ MCQs generated successfully!")
            st.subheader("📋 Generated MCQs")

            table_data = get_table_data(quiz)
            if table_data:
                df = pd.DataFrame(table_data)
                df.index = df.index + 1
                st.table(df)
            else:
                st.warning("Could not parse MCQ JSON. Raw output:")
                st.code(quiz, language="json")

            st.subheader("🧠 AI Review")
            st.info(review)

            with st.expander("📊 Token Usage & Cost"):
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Prompt Tokens",     cb.prompt_tokens)
                    st.metric("Completion Tokens",  cb.completion_tokens)
                with col2:
                    st.metric("Total Tokens", cb.total_tokens)
                    st.metric("Total Cost (USD)", f"${cb.total_cost:.6f}")

            logger.info(f"MCQs generated: {mcq_count} | Subject: {subject} | Tone: {tone}")

        except Exception as e:
            logger.error(str(e))
            st.error("❌ Error generating MCQs.")
            st.exception(e)