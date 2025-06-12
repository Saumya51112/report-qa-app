import streamlit as st
import fitz  # PyMuPDF
import docx
import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

st.set_page_config(page_title="Report Q&A App", layout="centered")
st.title("📄 GPT-Powered Report Q&A App")

def extract_text(file):
    ext = file.name.split('.')[-1].lower()
    text = ""
    if ext == "pdf":
        with fitz.open(stream=file.read(), filetype="pdf") as doc:
            for page in doc:
                text += page.get_text()
    elif ext == "docx":
        d = docx.Document(file)
        for para in d.paragraphs:
            text += para.text + "\n"
    elif ext == "txt":
        text = file.read().decode()
    else:
        st.warning("Unsupported file type.")
    return text

uploaded_file = st.file_uploader("Upload a .pdf, .docx, or .txt file", type=["pdf", "docx", "txt"])

if uploaded_file:
    with st.spinner("Reading your file..."):
        text = extract_text(uploaded_file)

    st.success("File processed!")
    st.text_area("Preview of extracted text:", text[:2000], height=250)

    question = st.text_input("What do you want to ask about this report?")
    if question:
        with st.spinner("Asking GPT..."):
            prompt = f"Answer this question based only on the following report:\n\n{text[:6000]}\n\nQuestion: {question}"
            from openai import OpenAI

client = OpenAI()

response = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": prompt}]
)

answer = response.choices[0].message.content

            answer = response.choices[0].message['content']
            st.markdown("### 🧠 GPT's Answer")
            st.write(answer)
