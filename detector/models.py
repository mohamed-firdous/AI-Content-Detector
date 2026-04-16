from __future__ import annotations

from functools import lru_cache

from sentence_transformers import SentenceTransformer

from detector.config import EMBEDDING_MODEL_NAME


@lru_cache(maxsize=1)
def get_embedding_model() -> SentenceTransformer:
    """Singleton model loader to avoid repeated downloads and cold starts."""
    return SentenceTransformer(EMBEDDING_MODEL_NAME)
