from __future__ import annotations

import json

import streamlit as st

from detector.pipeline import run_full_analysis
from detector.reporting import generate_pdf_report, generate_txt_report
from detector.visualization import build_heatmap_html, summarize_metrics, top_suspicious_rows


st.set_page_config(
    page_title="Academic Integrity Detector",
    page_icon="🧠",
    layout="wide",
)

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;700&family=Source+Serif+4:wght@400;600&display=swap');

    :root {
        --bg-soft: #f8f4ec;
        --card: #fffdf8;
        --text: #1d2a30;
        --accent: #0f766e;
        --accent-2: #d97706;
    }

    .stApp {
        background:
            radial-gradient(circle at 15% 10%, #ffe8c2 0%, transparent 30%),
            radial-gradient(circle at 80% 15%, #d5f5ef 0%, transparent 35%),
            linear-gradient(180deg, #f7f6f2 0%, var(--bg-soft) 100%);
    }

    h1, h2, h3 {
        font-family: 'Space Grotesk', sans-serif;
        color: var(--text);
        letter-spacing: -0.02em;
    }

    p, li, label, .stMarkdown, .stCaption {
        font-family: 'Source Serif 4', serif;
        color: #24343a;
    }

    [data-testid="stMetricValue"] {
        color: var(--accent);
    }

    [data-testid="stMetric"] {
        background: var(--card);
        border: 1px solid #dcd7cb;
        border-radius: 12px;
        padding: 12px;
    }

    .stButton > button {
        border-radius: 12px;
        border: 1px solid #0f766e;
        background: linear-gradient(120deg, #115e59, #0f766e);
        color: #fff;
    }

    .stDownloadButton > button {
        border-radius: 12px;
        border: 1px solid #c9bba0;
        background: #fffaf0;
        color: #4f3f25;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("Automated Academic Plagiarism & AI-Generated Content Detector")
st.caption("Hackathon MVP: fast, explainable paragraph-level integrity analysis")

with st.sidebar:
    st.subheader("Reference Corpus")
    custom_reference = st.text_area(
        "Paste reference corpus paragraphs (optional)",
        help="Each line will be treated as a reference text snippet.",
        height=180,
    )

    st.subheader("Performance Target")
    st.write("Expected analysis latency: under 20 seconds for typical assignment sizes.")

uploaded_file = st.file_uploader(
    "Upload assignment file",
    type=["pdf", "docx", "txt"],
    accept_multiple_files=False,
)

if uploaded_file:
    c1, c2 = st.columns([1, 4])
    with c1:
        run_clicked = st.button("Run Analysis", type="primary", use_container_width=True)
    with c2:
        st.info("The first run can take longer while downloading the embedding model.")

    if run_clicked:
        with st.spinner("Analyzing document..."):
            output = run_full_analysis(
                filename=uploaded_file.name,
                file_bytes=uploaded_file.getvalue(),
                extra_reference_text=custom_reference,
            )

        df = output.combined_df
        summary = summarize_metrics(df)

        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Paragraphs", summary["paragraph_count"])
        m2.metric("Avg Plagiarism", f"{summary['avg_plagiarism']:.2f}")
        m3.metric("Avg AI Probability", f"{summary['avg_ai_probability']:.2f}")
        m4.metric("High-Risk Sections", summary["high_risk_sections"])

        st.success(f"Analysis completed in {output.elapsed_seconds:.2f}s")
        if output.elapsed_seconds > 20:
            st.warning("Runtime exceeded 20s target. Consider reducing reference corpus size.")

        st.subheader("Suspicious Section Heatmap")
        st.markdown(build_heatmap_html(df), unsafe_allow_html=True)

        st.subheader("Top Suspicious Paragraphs")
        top_df = top_suspicious_rows(df)
        st.dataframe(
            top_df[[
                "paragraph_index",
                "risk_score",
                "plagiarism_score",
                "ai_probability",
                "plagiarism_confidence",
                "ai_confidence",
            ]],
            use_container_width=True,
        )

        st.subheader("Detailed Evidence Table")
        st.dataframe(df, use_container_width=True)

        txt_report = generate_txt_report(summary=summary, df=df, filename=output.filename)
        pdf_report = generate_pdf_report(summary=summary, df=df, filename=output.filename)

        d1, d2, d3 = st.columns(3)
        with d1:
            st.download_button(
                "Download TXT Report",
                data=txt_report,
                file_name="integrity_report.txt",
                mime="text/plain",
                use_container_width=True,
            )
        with d2:
            st.download_button(
                "Download PDF Report",
                data=pdf_report,
                file_name="integrity_report.pdf",
                mime="application/pdf",
                use_container_width=True,
            )
        with d3:
            st.download_button(
                "Download JSON",
                data=json.dumps(df.to_dict(orient="records"), indent=2),
                file_name="integrity_report.json",
                mime="application/json",
                use_container_width=True,
            )

else:
    st.info("Upload a PDF, DOCX, or TXT assignment file to begin analysis.")

st.markdown("---")
st.caption("For academic triage only. Final misconduct decisions should include faculty review.")
