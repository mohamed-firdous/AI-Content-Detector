def split_into_paragraphs(text):
    """
    Splits a raw text body into discrete paragraphs using newline characters.
    It filters out completely empty lines and sentences that possess fewer than 40 characters.
    
    Returns:
        List of cleaned paragraph strings.
    """
    if not text:
        return []

    # Split text line-by-line primarily separating blocks based on newlines 
    raw_paragraphs = text.split('\n')
    
    cleaned_paragraphs = []
    
    for p in raw_paragraphs:
        cleaned = p.strip()
        # Keep paragraph if it has 40 or more characters and is not purely whitespace
        if len(cleaned) >= 40:
            cleaned_paragraphs.append(cleaned)
            
    return cleaned_paragraphs
