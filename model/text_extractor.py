import os
from pdfminer.high_level import extract_text as extract_pdf_text
import docx

def extract_text_from_pdf(file_path):
    """
    Extracts plain text from a given PDF file using pdfminer.six.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
        
    try:
        text = extract_pdf_text(file_path)
        return text if text else ""
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        return ""


def extract_text_from_docx(file_path):
    """
    Extracts text from a given DOCX file using python-docx.
    Iterates through all paragraphs in the document and joins them.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
        
    try:
        doc = docx.Document(file_path)
        paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]
        return "\n".join(paragraphs)
    except Exception as e:
        print(f"Error extracting text from DOCX: {e}")
        return ""
