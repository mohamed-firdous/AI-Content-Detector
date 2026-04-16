from __future__ import annotations

import math
import re
from dataclasses import dataclass
from statistics import mean, pstdev
from typing import List, Sequence

import numpy as np
import nltk
from nltk.corpus import stopwords

from detector.config import AI_HIGH_THRESHOLD, AI_MEDIUM_THRESHOLD


@dataclass
class AIDetectionResult:
    paragraph_index: int
    ai_probability: float
    confidence_label: str
    burstiness: float
    lexical_diversity: float
    punctuation_density: float
    entropy_proxy: float


_STOPWORDS = None


def _ensure_nltk() -> None:
    global _STOPWORDS
    if _STOPWORDS is not None:
        return
    try:
        nltk.data.find("corpora/stopwords")
    except LookupError:
        nltk.download("stopwords", quiet=True)
    _STOPWORDS = set(stopwords.words("english"))


def _label(probability: float) -> str:
    if probability >= AI_HIGH_THRESHOLD:
        return "High"
    if probability >= AI_MEDIUM_THRESHOLD:
        return "Medium"
    return "Low"


def _safe_entropy(text: str) -> float:
    if not text:
        return 0.0
    counts = {}
    for ch in text.lower():
        counts[ch] = counts.get(ch, 0) + 1
    total = len(text)
    entropy = 0.0
    for c in counts.values():
        p = c / total
        entropy -= p * math.log2(p)
    return entropy


def _stylometric_features(paragraph: str) -> dict:
    tokens = re.findall(r"\b\w+\b", paragraph.lower())
    sentences = [s.strip() for s in re.split(r"[.!?]+", paragraph) if s.strip()]
    punct = re.findall(r"[,:;!?]", paragraph)

    if not tokens:
        return {
            "lexical_diversity": 0.0,
            "stopword_ratio": 0.0,
            "sentence_length_mean": 0.0,
            "sentence_length_std": 0.0,
            "punctuation_density": 0.0,
            "entropy": 0.0,
        }

    sentence_lengths = [len(re.findall(r"\b\w+\b", s)) for s in sentences] or [len(tokens)]
    lexical_diversity = len(set(tokens)) / max(len(tokens), 1)
    stopword_ratio = sum(1 for t in tokens if t in _STOPWORDS) / max(len(tokens), 1)

    return {
        "lexical_diversity": lexical_diversity,
        "stopword_ratio": stopword_ratio,
        "sentence_length_mean": mean(sentence_lengths),
        "sentence_length_std": pstdev(sentence_lengths) if len(sentence_lengths) > 1 else 0.0,
        "punctuation_density": len(punct) / max(len(tokens), 1),
        "entropy": _safe_entropy(paragraph),
    }


def _score_probability(features: dict) -> float:
    # Weighted heuristic for MVP explainability.
    lexical_signal = 1.0 - np.clip(features["lexical_diversity"], 0.0, 1.0)
    burstiness_signal = 1.0 - np.clip(features["sentence_length_std"] / 25.0, 0.0, 1.0)
    entropy_signal = 1.0 - np.clip(features["entropy"] / 5.2, 0.0, 1.0)
    punctuation_signal = 1.0 - np.clip(features["punctuation_density"] / 0.25, 0.0, 1.0)
    stopword_signal = np.clip(abs(features["stopword_ratio"] - 0.48) * 2.4, 0.0, 1.0)

    probability = (
        0.28 * lexical_signal
        + 0.24 * burstiness_signal
        + 0.22 * entropy_signal
        + 0.14 * punctuation_signal
        + 0.12 * stopword_signal
    )
    return float(np.clip(probability, 0.0, 1.0))


def detect_ai_generated_content(paragraphs: Sequence[str]) -> List[AIDetectionResult]:
    _ensure_nltk()

    results: List[AIDetectionResult] = []
    for idx, paragraph in enumerate(paragraphs):
        features = _stylometric_features(paragraph)
        probability = _score_probability(features)
        burstiness = float(np.clip(features["sentence_length_std"] / 20.0, 0.0, 1.0))

        results.append(
            AIDetectionResult(
                paragraph_index=idx,
                ai_probability=round(probability, 4),
                confidence_label=_label(probability),
                burstiness=round(burstiness, 4),
                lexical_diversity=round(features["lexical_diversity"], 4),
                punctuation_density=round(features["punctuation_density"], 4),
                entropy_proxy=round(features["entropy"], 4),
            )
        )

    return results
