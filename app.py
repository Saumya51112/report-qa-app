import streamlit as st
import fitz  # PyMuPDF
import docx
from openai import OpenAI
import os

# Initialize OpenAI client using API key from GitHub secrets
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Streamlit page setup
st.set_page_config(page_title="Report Q&A Chatbot", layout="centered")
st.title("📄 Chat with Your Report (Powered by GPT-4)")

# Function to extract text from uploaded document
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

# Upload file
uploaded_file = st.file_uploader("📤 Upload a report (.pdf, .docx, .txt)", type=["pdf", "docx", "txt"])

if uploaded_file:
    with st.spinner("📄 Reading and parsing the file..."):
        document_text = extract_text(uploaded_file)

    st.success("✅ File successfully processed!")
    st.text_area("📃 Preview of Extracted Text:", document_text[:2000], height=200)

    # Initialize chat history in session state
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = [
            {"role": "system", "content": "You are a helpful assistant answering questions based only on the uploaded report."},
            {"role": "user", "content": f"Here is the report:\n\n{document_text[:6000]}"}
        ]

    # Chat interface
    user_question = st.chat_input("💬 Ask a question about the report...")

    if user_question:
        # Add user message to history
        st.session_state.chat_history.append({"role": "user", "content": user_question})

        with st.spinner("🤖 GPT is thinking..."):
            response = client.chat.completions.create(
                model="gpt-4",
                me
