import os
import glob
from sentence_transformers import SentenceTransformer, util
import torch

# Initialize model globally to optimize runtime across multiple paragraph requests.
try:
    model = SentenceTransformer('all-MiniLM-L6-v2')
except Exception as e:
    print(f"Warning: Could not load SentenceTransformer model. {e}")
    model = None

# Reference articles store
REFERENCE_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'sample_data', 'reference_articles')
reference_embeddings = None

def load_references():
    """
    Loads all .txt contents from the reference_articles directory and 
    caches them as tensor embeddings for subsequent rapid similarity matching.
    """
    global reference_embeddings
    if reference_embeddings is not None or not model:
        return
    
    if not os.path.exists(REFERENCE_DIR):
        print(f"Warning: Reference directory missing at {REFERENCE_DIR}")
        return
        
    reference_texts = []
    for filepath in glob.glob(os.path.join(REFERENCE_DIR, '*.txt')):
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                if content:
                    reference_texts.append(content)
        except Exception as e:
            print(f"Failed to read file {filepath}: {e}")
                
    if reference_texts:
        # Pre-compute all known vectors to optimize execution times drastically.
        reference_embeddings = model.encode(reference_texts, convert_to_tensor=True)

# Pre-load knowledge base into VRAM / RAM at startup
load_references()

def compute_plagiarism_score(paragraph):
    """
    Generates an embedding for the source paragraph and computes the max cosine similarity
    score against all internal reference embeddings.
    
    Returns:
        float: Similarity probability score mapped [0.0, 1.0].
    """
    if not paragraph.strip() or not model or reference_embeddings is None or len(reference_embeddings) == 0:
        return 0.0
        
    try:
        # Generate the vector payload
        paragraph_emb = model.encode(paragraph, convert_to_tensor=True)
        
        # Produce a tensor mapping the individual paragraph against every reference block natively
        cosine_scores = util.cos_sim(paragraph_emb, reference_embeddings)
        
        # We assume the maximum detected correlation reflects the final "plagiarism" scale.
        max_score = torch.max(cosine_scores).item()
        
        # Round intelligently and clamp between 0.0 and 1.0 bounds
        clamped_val = max(0.0, min(1.0, max_score))
        return round(clamped_val, 2)
        
    except Exception as e:
        print(f"Error computing plagiarism score: {e}")
        return 0.0
