# app/utils/file_handler.py
from PyPDF2 import PdfReader

def extract_text_from_pdf(pdf_file):
    """
    Extract text content from a PDF file using PyPDF2.
    Args:
        pdf_file: File object of the uploaded PDF
    Returns:
        str: Extracted text from the PDF
    """
    text = ""
    reader = PdfReader(pdf_file)
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text.strip()