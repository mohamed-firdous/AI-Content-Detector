from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
DEFAULT_REFERENCE_CORPUS = DATA_DIR / "reference_corpus.txt"

EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
SIMILARITY_THRESHOLD = 0.78

# Kept conservative for hackathon speed and explainability.
AI_HIGH_THRESHOLD = 0.72
AI_MEDIUM_THRESHOLD = 0.45
PLAGIARISM_HIGH_THRESHOLD = 0.8
PLAGIARISM_MEDIUM_THRESHOLD = 0.55
