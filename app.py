import streamlit as st
import pdfplumber
from docx import Document
from collections import Counter
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import re

# Extract text from PDF using pdfplumber
def extract_text_from_pdf(file):
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text

# Extract text from DOCX
def extract_text_from_docx(file):
    doc = Document(file)
    return "\n".join([para.text for para in doc.paragraphs])

# Clean and tokenize text
def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-z\s]', '', text)
    words = text.split()
    return words

# Streamlit UI
st.title("📄 PDF/DOCX Text Visualizer")
uploaded_file = st.file_uploader("Upload a PDF or DOCX file", type=["pdf", "docx"])

if uploaded_file:
    if uploaded_file.name.endswith(".pdf"):
        raw_text = extract_text_from_pdf(uploaded_file)
    else:
        raw_text = extract_text_from_docx(uploaded_file)

    words = clean_text(raw_text)
    word_freq = Counter(words)
    top_words = word_freq.most_common(20)

    # Bar chart
    st.subheader("🔢 Top 20 Word Frequencies")
    words_list, freq_list = zip(*top_words)
    fig, ax = plt.subplots()
    ax.bar(words_list, freq_list, color='skyblue')
    plt.xticks(rotation=45)
    st.pyplot(fig)

    # Word cloud
    st.subheader("☁️ Word Cloud")
    wc = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(word_freq)
    fig_wc, ax_wc = plt.subplots()
    ax_wc.imshow(wc, interpolation='bilinear')
    ax_wc.axis('off')
    st.pyplot(fig_wc)
