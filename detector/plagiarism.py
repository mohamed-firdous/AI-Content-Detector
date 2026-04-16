from __future__ import annotations

from dataclasses import dataclass
from typing import List, Sequence

import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

from detector.config import PLAGIARISM_HIGH_THRESHOLD, PLAGIARISM_MEDIUM_THRESHOLD, SIMILARITY_THRESHOLD
from detector.models import get_embedding_model


@dataclass
class PlagiarismResult:
    paragraph_index: int
    plagiarism_score: float
    confidence_label: str
    matched_reference: str
    matched_reference_index: int


def _label(score: float) -> str:
    if score >= PLAGIARISM_HIGH_THRESHOLD:
        return "High"
    if score >= PLAGIARISM_MEDIUM_THRESHOLD:
        return "Medium"
    return "Low"


def detect_plagiarism(
    paragraphs: Sequence[str],
    reference_paragraphs: Sequence[str],
) -> List[PlagiarismResult]:
    if not paragraphs:
        return []

    if not reference_paragraphs:
        reference_paragraphs = [
            "No external reference corpus supplied; score estimated against minimal baseline text."
        ]

    model = get_embedding_model()
    para_embeddings = model.encode(list(paragraphs), batch_size=32, show_progress_bar=False, normalize_embeddings=True)
    ref_embeddings = model.encode(list(reference_paragraphs), batch_size=32, show_progress_bar=False, normalize_embeddings=True)

    sim_matrix = cosine_similarity(para_embeddings, ref_embeddings)

    results: List[PlagiarismResult] = []
    for idx in range(sim_matrix.shape[0]):
        best_ref_idx = int(np.argmax(sim_matrix[idx]))
        best_score = float(sim_matrix[idx, best_ref_idx])
        scaled_score = min(1.0, best_score / max(SIMILARITY_THRESHOLD, 1e-6))
        results.append(
            PlagiarismResult(
                paragraph_index=idx,
                plagiarism_score=round(scaled_score, 4),
                confidence_label=_label(scaled_score),
                matched_reference=reference_paragraphs[best_ref_idx],
                matched_reference_index=best_ref_idx,
            )
        )

    return results
