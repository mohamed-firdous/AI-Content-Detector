from detector.ai_detector import detect_ai_generated_content
from detector.file_processing import split_into_paragraphs
from detector.plagiarism import detect_plagiarism


def test_split_into_paragraphs_merges_short_chunks():
    text = "Short.\n\nThis is a sufficiently long paragraph for testing purposes with enough tokens to pass threshold."
    paragraphs = split_into_paragraphs(text, min_chars=20)
    assert len(paragraphs) == 1


def test_ai_detector_returns_probabilities():
    paragraphs = [
        "This paragraph contains clear claims and varied sentence structures, plus examples and references.",
        "Therefore this paragraph is concise and predictable in style.",
    ]
    results = detect_ai_generated_content(paragraphs)
    assert len(results) == 2
    assert 0 <= results[0].ai_probability <= 1


def test_plagiarism_detects_similarity_shape():
    paragraphs = ["Machine learning assignments require datasets and validation strategy."]
    refs = ["Machine learning assignments often require documenting dataset origin and validation strategy."]
    results = detect_plagiarism(paragraphs, refs)
    assert len(results) == 1
    assert 0 <= results[0].plagiarism_score <= 1
