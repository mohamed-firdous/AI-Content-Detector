from __future__ import annotations

import time
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import List, Optional, Sequence

import pandas as pd

from detector.ai_detector import AIDetectionResult, detect_ai_generated_content
from detector.config import DEFAULT_REFERENCE_CORPUS
from detector.file_processing import ParsedDocument, parse_uploaded_file
from detector.plagiarism import PlagiarismResult, detect_plagiarism


@dataclass
class AnalysisOutput:
    filename: str
    elapsed_seconds: float
    paragraphs: List[str]
    plagiarism_results: List[PlagiarismResult]
    ai_results: List[AIDetectionResult]
    combined_df: pd.DataFrame


def load_reference_corpus(extra_text: Optional[str] = None) -> List[str]:
    corpus: List[str] = []

    if Path(DEFAULT_REFERENCE_CORPUS).exists():
        with open(DEFAULT_REFERENCE_CORPUS, "r", encoding="utf-8") as f:
            corpus.extend([line.strip() for line in f if line.strip()])

    if extra_text and extra_text.strip():
        corpus.extend([p.strip() for p in extra_text.split("\n") if p.strip()])

    return corpus


def _build_combined_frame(
    paragraphs: Sequence[str],
    plagiarism_results: Sequence[PlagiarismResult],
    ai_results: Sequence[AIDetectionResult],
) -> pd.DataFrame:
    rows = []
    for idx, paragraph in enumerate(paragraphs):
        pl = plagiarism_results[idx]
        ai = ai_results[idx]
        risk_score = round((0.58 * pl.plagiarism_score) + (0.42 * ai.ai_probability), 4)
        rows.append(
            {
                "paragraph_index": idx + 1,
                "paragraph": paragraph,
                "plagiarism_score": pl.plagiarism_score,
                "plagiarism_confidence": pl.confidence_label,
                "matched_reference": pl.matched_reference,
                "ai_probability": ai.ai_probability,
                "ai_confidence": ai.confidence_label,
                "risk_score": risk_score,
            }
        )

    return pd.DataFrame(rows)


def run_full_analysis(
    filename: str,
    file_bytes: bytes,
    extra_reference_text: Optional[str] = None,
) -> AnalysisOutput:
    started = time.perf_counter()

    parsed: ParsedDocument = parse_uploaded_file(filename=filename, file_bytes=file_bytes)
    reference_corpus = load_reference_corpus(extra_text=extra_reference_text)

    plagiarism_results = detect_plagiarism(parsed.paragraphs, reference_corpus)
    ai_results = detect_ai_generated_content(parsed.paragraphs)
    combined_df = _build_combined_frame(parsed.paragraphs, plagiarism_results, ai_results)

    elapsed = round(time.perf_counter() - started, 3)
    return AnalysisOutput(
        filename=parsed.filename,
        elapsed_seconds=elapsed,
        paragraphs=parsed.paragraphs,
        plagiarism_results=plagiarism_results,
        ai_results=ai_results,
        combined_df=combined_df,
    )


def to_serializable_summary(output: AnalysisOutput) -> dict:
    return {
        "filename": output.filename,
        "elapsed_seconds": output.elapsed_seconds,
        "rows": output.combined_df.to_dict(orient="records"),
        "plagiarism_results": [asdict(item) for item in output.plagiarism_results],
        "ai_results": [asdict(item) for item in output.ai_results],
    }
