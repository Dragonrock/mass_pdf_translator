import streamlit as st
from googletrans import Translator
from PyPDF2 import PdfReader, PdfWriter
from fpdf import FPDF
import io
import os

def extract_text_from_pdf(pdf_file):
    reader = PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text

def translate_text(text, dest_lang='en'):
    translator = Translator()
    translated = translator.translate(text, dest=dest_lang)
    return translated.text

def create_translated_pdf(translated_text, original_pdf):
    # Create a new PDF with similar structure
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    # Add translated text
    pdf.multi_cell(0, 10, translated_text)
    
    # Save to bytes buffer
    buffer = io.BytesIO()
    pdf.output(buffer)
    buffer.seek(0)
    return buffer

def main():
    st.title("PDF Translator")
    
    # Language selection
    dest_lang = st.selectbox("Select Target Language", ['en', 'es', 'fr', 'de', 'el'])
    
    # File upload
    uploaded_files = st.file_uploader("Upload PDF files", type="pdf", accept_multiple_files=True)
    
    if uploaded_files:
        for uploaded_file in uploaded_files:
            with st.spinner(f'Processing {uploaded_file.name}...'):
                # Extract text
                text = extract_text_from_pdf(uploaded_file)
                
                # Translate text
                translated_text = translate_text(text, dest_lang)
                
                # Create translated PDF
                translated_pdf = create_translated_pdf(translated_text, uploaded_file)
                
                # Download button
                st.download_button(
                    label=f"Download Translated {uploaded_file.name}",
                    data=translated_pdf,
                    file_name=f"translated_{uploaded_file.name}",
                    mime="application/pdf"
                )

if __name__ == "__main__":
    main()
