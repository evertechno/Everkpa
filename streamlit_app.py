import streamlit as st
import time
from io import StringIO
import PyPDF2

# Mock function for AI model or API call (replace with your actual function)
def process_document(file):
    # Example processing: just returns a simple summary or message.
    time.sleep(2)  # Simulate a processing delay (e.g., AI model inference time)
    if file.name.endswith(".txt"):
        content = file.getvalue().decode("utf-8")
        return f"Text file processed. Length of content: {len(content)} characters."
    elif file.name.endswith(".pdf"):
        # Read the first page of the PDF for simplicity
        pdf_reader = PyPDF2.PdfReader(file)
        first_page = pdf_reader.pages[0].extract_text()
        return f"PDF processed. First page content: {first_page[:200]}..."  # Preview first 200 characters
    else:
        return "Unsupported file format. Please upload a .txt or .pdf file."

# Streamlit UI components
st.title("Document Processing with AI")
st.write("Upload a document (txt or pdf) for processing.")

# File uploader
uploaded_file = st.file_uploader("Choose a file", type=["txt", "pdf"])

if uploaded_file is not None:
    # Display the uploaded file name
    st.write(f"Uploaded file: {uploaded_file.name}")
    
    # Display file preview for text files
    if uploaded_file.name.endswith(".txt"):
        file_content = uploaded_file.getvalue().decode("utf-8")
        st.text_area("File Preview", file_content, height=150)
    
    elif uploaded_file.name.endswith(".pdf"):
        # PDF file preview (first 200 characters of the first page)
        with open(uploaded_file.name, "wb") as f:
            f.write(uploaded_file.getvalue())
        st.text_area("File Preview", "First 200 characters of the PDF: " + process_document(uploaded_file)[:200], height=150)
    
    # Button to trigger the processing
    if st.button("Process File"):
        with st.spinner('Processing your file...'):
            result = process_document(uploaded_file)
        
        # Display the processed result
        st.success("File processed successfully!")
        st.write(result)

# Additional UI for text input if no file is uploaded
else:
    st.write("Or, input some text directly for processing.")
    user_input = st.text_area("Enter your text here", height=200)
    
    # Process button for manual text input
    if st.button("Process Text"):
        if user_input.strip():
            with st.spinner('Processing your input text...'):
                time.sleep(2)  # Simulating processing time
                st.success("Text processed successfully!")
                st.write(f"Processed text: {user_input[:200]}...")  # Show a preview of the processed text
        else:
            st.warning("Please enter some text before processing.")
