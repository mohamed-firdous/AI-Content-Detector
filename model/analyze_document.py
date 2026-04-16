import os
import json
try:
    from .text_extractor import extract_text_from_pdf, extract_text_from_docx
    from .paragraph_splitter import split_into_paragraphs
    from .plagiarism_model import compute_plagiarism_score
    from .ai_detector import compute_ai_probability
except ImportError:
    # Direct execution overrides
    from text_extractor import extract_text_from_pdf, extract_text_from_docx
    from paragraph_splitter import split_into_paragraphs
    from plagiarism_model import compute_plagiarism_score
    from ai_detector import compute_ai_probability

def analyze_document(file_path):
    """
    Main integration pipeline.
    Parses a file path and orchestrates the extraction, splitting, and multi-model inferences.
    
    Returns:
        dict: A strict JSON structure conveying normalized plagiarism and ai prediction scores.
    """
    if not os.path.exists(file_path):
        return {"error": "File not found"}
        
    ext = file_path.lower().split('.')[-1]
    
    # 1. Extraction Layer
    raw_text = ""
    if ext == 'pdf':
        raw_text = extract_text_from_pdf(file_path)
    elif ext == 'docx':
        raw_text = extract_text_from_docx(file_path)
    elif ext == 'txt':
        # Adding minimal support for raw text specifically to run immediate tests utilizing sample articles.
        with open(file_path, 'r', encoding='utf-8') as f:
            raw_text = f.read()
    else:
        return {"error": f"Unsupported file type '{ext}'"}

    # Guard check for unreadable formats mapping to empty payloads.
    if not raw_text.strip():
        return {"error": "No extractable text found"}
        
    # 2. Preprocessing / Sub-splitting
    paragraphs = split_into_paragraphs(raw_text)
    if not paragraphs:
        return {"error": "No valid paragraphs found"}
        
    # 3. Model Inferencing
    paragraph_analysis = []
    total_plag = 0.0
    total_ai = 0.0
    
    for p in paragraphs:
        p_score = compute_plagiarism_score(p)
        a_score = compute_ai_probability(p)
        
        total_plag += p_score
        total_ai += a_score
        
        paragraph_analysis.append({
            "paragraph": p,
            "plagiarism_score": p_score,
            "ai_probability": a_score
        })
        
    # 4. Global Average Construction
    overall_plag = round(total_plag / len(paragraphs), 2)
    overall_ai = round(total_ai / len(paragraphs), 2)
    
    payload = {
        "overall_plagiarism_score": overall_plag,
        "overall_ai_probability": overall_ai,
        "paragraph_analysis": paragraph_analysis
    }
    
    return payload
