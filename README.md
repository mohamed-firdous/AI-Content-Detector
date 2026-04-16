# Automated Academic Plagiarism & AI-Generated Content Detector

A hackathon-ready Streamlit MVP that analyzes student submissions (PDF, DOCX, TXT) for:
- Paragraph-level plagiarism risk (semantic similarity + sentence embeddings)
- Paragraph-level AI-generation probability (stylometric heuristic)
- Explainable evidence with heatmap and matched references
- Downloadable faculty-facing reports (TXT, PDF, JSON)

## Architecture

- `app.py`: Streamlit UI and orchestration
- `detector/file_processing.py`: PDF/DOCX/TXT parsing and text cleanup
- `detector/plagiarism.py`: Embedding-based plagiarism detection
- `detector/ai_detector.py`: Stylometric AI-content detection
- `detector/visualization.py`: Heatmap and suspicious section summaries
- `detector/reporting.py`: TXT/PDF report generation
- `detector/pipeline.py`: End-to-end analysis pipeline
- `data/reference_corpus.txt`: Baseline reference corpus

## Quick Start

```bash
pip install -r requirements.txt
streamlit run app.py
```

Then open the local URL printed by Streamlit.

## Docker Deployment

```bash
docker build -t academic-integrity-detector .
docker run -p 8501:8501 academic-integrity-detector
```

Then open `http://localhost:8501`.

## Detection Logic

### Plagiarism Engine
- Uses `sentence-transformers/all-MiniLM-L6-v2` embeddings
- Computes cosine similarity between assignment paragraphs and reference corpus
- Outputs paragraph-level score and top matched reference evidence

### AI Detection Engine
- Uses stylometric features:
  - lexical diversity
  - stopword ratio
  - punctuation density
  - sentence-length burstiness proxy
  - entropy-based perplexity proxy
- Converts weighted features into paragraph-level AI probability

## Performance Notes

- First run can be slower due to model download.
- Subsequent runs are faster via model caching.
- For under-20-second target, keep reference corpus concise.

## Testing

```bash
pytest -q
```

## Runtime Benchmark

```bash
python scripts/benchmark.py path/to/sample_assignment.txt --runs 3
```

This helps validate the under-20-second analysis target on your machine.

## What Is Fully Implemented

- Upload support: PDF, DOCX, TXT
- Clean text extraction and paragraph segmentation
- Embedding-based plagiarism scoring with matched evidence
- Paragraph-level AI probability (stylometric heuristic)
- Combined risk score and evidence heatmap
- Faculty-facing TXT, PDF, and JSON downloadable reports
- Smoke tests and benchmark utility
- Local and Docker deployment options

## MVP Constraints

- AI probability is heuristic and should be interpreted as triage signal, not proof.
- Plagiarism comparison quality depends on reference corpus quality.
