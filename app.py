import streamlit as st
import fitz  # PyMuPDF
import docx
from openai import OpenAI
import os

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.set_page_config(page_title="Report Q&A App", layout="centered")
st.title("📄 GPT-Powered Report Q&A")

# Function to extract text from uploaded file
def extract_text(file):
    ext = file.name.split('.')[-1].lower()
    text = ""

    if ext == "pdf":
        with fitz.open(stream=file.read(), filetype="pdf") as doc:
            for page in doc:
                text += page.get_text()

    elif ext == "docx":
        doc_file = docx.Document(file)
        for para in doc_file.paragraphs:
            text += para.text + "\n"

    elif ext == "txt":
        text = file.read().decode()

    else:
        st.warning("Unsupported file type.")
    
    return text

# File uploader
uploaded_file = st.file_uploader("Upload a report (.pdf, .docx, .txt)", type=["pdf", "docx", "txt"])

if uploaded_file:
    with st.spinner("📄 Reading and parsing the file..."):
        document_text = extract_text(uploaded_file)

    st.success("✅ File successfully processed!")
    st.text_area("📃 Preview of Extracted Text:", document_text[:2000], height=250)

    # Question input
    question = st.text_input("💬 Ask a question about the report:")

    if question:
        with st.spinner("🤖 GPT is thinking..."):
            prompt = f"""Answer this question based only on the following report:\n\n{document_text[:6000]}\n\nQuestion: {question}"""

            response = client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}]
            )

            answer = response.choices[0].message.content

        st.markdown("### 🧠 GPT's Answer:")
        st.write(answer)
