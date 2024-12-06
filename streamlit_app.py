import streamlit as st
import time
from io import StringIO
import PyPDF2
from PIL import Image
from wordcloud import WordCloud
import io
import pandas as pd
import langdetect
from textblob import TextBlob
import spacy
import requests
import zipfile
import os
import pyttsx3
from io import BytesIO
import difflib

# Initialize spacy model for NER
nlp = spacy.load("en_core_web_sm")

# Mock AI processing function (replace with real processing logic)
def process_document(file):
    time.sleep(2)  # Simulate processing delay
    if file.name.endswith(".txt"):
        content = file.getvalue().decode("utf-8")
        return content
    elif file.name.endswith(".pdf"):
        pdf_reader = PyPDF2.PdfReader(file)
        first_page = pdf_reader.pages[0].extract_text()
        return first_page
    else:
        return None

# Feature to show word cloud
def generate_word_cloud(text):
    wordcloud = WordCloud(width=800, height=400, background_color="white").generate(text)
    return wordcloud

# Sentiment analysis with TextBlob
def sentiment_analysis(text):
    analysis = TextBlob(text)
    return analysis.sentiment

# Named Entity Recognition (NER)
def named_entity_recognition(text):
    doc = nlp(text)
    entities = [(entity.text, entity.label_) for entity in doc.ents]
    return entities

# Language detection
def detect_language(text):
    lang = langdetect.detect(text)
    return lang

# Text summarization (basic method)
def summarize_text(text, word_count=100):
    words = text.split()
    summary = ' '.join(words[:word_count])
    return summary

# File download function
def download_file(content, filename, mime_type):
    st.download_button("Download Processed File", content=content, file_name=filename, mime=mime_type)

# Text-to-Speech
def text_to_speech(text):
    engine = pyttsx3.init()
    engine.save_to_file(text, "output.mp3")
    return "output.mp3"

# Display Document Comparison
def compare_documents(text1, text2):
    diff = difflib.ndiff(text1.splitlines(), text2.splitlines())
    return '\n'.join(diff)

# Main Streamlit UI
st.title("Advanced Document Processing with AI")
st.write("Upload a document (txt, pdf, image) for processing.")

# File uploader
uploaded_file = st.file_uploader("Choose a file", type=["txt", "pdf", "jpg", "jpeg", "png"])

if uploaded_file is not None:
    st.write(f"Uploaded file: {uploaded_file.name}")

    # Progress Bar for processing
    progress_bar = st.progress(0)
    for i in range(100):
        time.sleep(0.05)
        progress_bar.progress(i + 1)

    # File preview and processing
    file_content = None
    if uploaded_file.name.endswith(".txt"):
        file_content = uploaded_file.getvalue().decode("utf-8")
        st.text_area("File Preview", file_content[:500], height=150)

    elif uploaded_file.name.endswith(".pdf"):
        file_content = process_document(uploaded_file)
        st.text_area("PDF Preview", file_content[:500], height=150)

    elif uploaded_file.name.endswith((".jpg", ".jpeg", ".png")):
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)
        st.write("Performing OCR...")  # Placeholder for OCR processing if implemented

    # Document processing
    if file_content:
        st.subheader("Text Analysis")
        word_count = len(file_content.split())
        sentence_count = len(file_content.split('.'))
        st.write(f"Word Count: {word_count}")
        st.write(f"Sentence Count: {sentence_count}")
        st.write(f"Readability Score: 58.7 (example)")  # Replace with actual calculation

        # Sentiment Analysis
        sentiment = sentiment_analysis(file_content)
        st.write(f"Sentiment Analysis: Polarity = {sentiment.polarity}, Subjectivity = {sentiment.subjectivity}")

        # Named Entity Recognition (NER)
        entities = named_entity_recognition(file_content)
        st.write(f"Named Entities: {entities}")

        # Language Detection
        language = detect_language(file_content)
        st.write(f"Detected Language: {language}")

        # Text Summarization
        summary = summarize_text(file_content, word_count=100)
        st.write(f"Summary: {summary}")

        # Word Cloud
        wordcloud = generate_word_cloud(file_content)
        st.image(wordcloud.to_array(), caption="Word Cloud")

        # Text-to-Speech
        audio_file = text_to_speech(file_content)
        st.audio(audio_file)

    # Options for downloading processed file
    if file_content:
        download_file(file_content, "processed_text.txt", "text/plain")

    # Compare documents if multiple files are uploaded
    uploaded_file2 = st.file_uploader("Upload a second document for comparison", type=["txt", "pdf"])
    if uploaded_file2 is not None:
        file_content2 = process_document(uploaded_file2)
        if file_content2:
            diff = compare_documents(file_content, file_content2)
            st.subheader("Document Comparison")
            st.text_area("Differences", diff, height=200)

# Multiple files and file size validation
if uploaded_file:
    st.write(f"File size: {uploaded_file.size / 1024:.2f} KB")
    if uploaded_file.size > 5 * 1024 * 1024:  # 5MB size limit
        st.warning("File is too large! Please upload a file smaller than 5MB.")

    if st.button("Process Document"):
        with st.spinner("Processing..."):
            time.sleep(3)
            st.success("Document processed!")

else:
    st.warning("Please upload a file to start processing.")
