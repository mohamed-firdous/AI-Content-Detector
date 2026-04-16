from __future__ import annotations

from datetime import datetime
from io import BytesIO
from typing import Dict

import pandas as pd
from fpdf import FPDF


def generate_txt_report(summary: Dict, df: pd.DataFrame, filename: str) -> str:
    lines = [
        "Automated Academic Plagiarism & AI-Generated Content Detector",
        f"Generated: {datetime.utcnow().isoformat()} UTC",
        f"Source file: {filename}",
        "",
        "Summary Metrics",
        f"- Total paragraphs: {summary['paragraph_count']}",
        f"- Average plagiarism score: {summary['avg_plagiarism']:.3f}",
        f"- Average AI probability: {summary['avg_ai_probability']:.3f}",
        f"- High risk sections: {summary['high_risk_sections']}",
        "",
        "Detailed Findings",
    ]

    for _, row in df.iterrows():
        lines.extend(
            [
                f"Paragraph {int(row['paragraph_index'])}",
                f"Risk Score: {row['risk_score']:.3f}",
                f"Plagiarism: {row['plagiarism_score']:.3f} ({row['plagiarism_confidence']})",
                f"AI Probability: {row['ai_probability']:.3f} ({row['ai_confidence']})",
                f"Matched Evidence: {row['matched_reference']}",
                f"Text: {row['paragraph'][:400]}",
                "",
            ]
        )

    return "\n".join(lines)


def generate_pdf_report(summary: Dict, df: pd.DataFrame, filename: str) -> bytes:
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    pdf.set_font("Helvetica", "B", 14)
    pdf.multi_cell(0, 8, "Academic Plagiarism and AI Content Detection Report")

    pdf.set_font("Helvetica", size=10)
    pdf.multi_cell(0, 6, f"Generated: {datetime.utcnow().isoformat()} UTC")
    pdf.multi_cell(0, 6, f"Source file: {filename}")
    pdf.ln(3)

    pdf.set_font("Helvetica", "B", 11)
    pdf.cell(0, 7, "Summary Metrics", ln=True)
    pdf.set_font("Helvetica", size=10)
    pdf.multi_cell(0, 6, f"Total paragraphs: {summary['paragraph_count']}")
    pdf.multi_cell(0, 6, f"Average plagiarism score: {summary['avg_plagiarism']:.3f}")
    pdf.multi_cell(0, 6, f"Average AI probability: {summary['avg_ai_probability']:.3f}")
    pdf.multi_cell(0, 6, f"High risk sections: {summary['high_risk_sections']}")

    pdf.ln(2)
    pdf.set_font("Helvetica", "B", 11)
    pdf.cell(0, 7, "Top suspicious sections", ln=True)

    pdf.set_font("Helvetica", size=9)
    for _, row in df.sort_values("risk_score", ascending=False).head(10).iterrows():
        pdf.multi_cell(
            0,
            5,
            (
                f"Paragraph {int(row['paragraph_index'])} | Risk={row['risk_score']:.3f} "
                f"| Plag={row['plagiarism_score']:.3f} | AI={row['ai_probability']:.3f}"
            ),
        )
        pdf.multi_cell(0, 5, f"Evidence: {row['matched_reference'][:220]}")
        pdf.multi_cell(0, 5, f"Excerpt: {row['paragraph'][:220]}")
        pdf.ln(1)

    raw = pdf.output(dest="S")
    if isinstance(raw, bytearray):
        return bytes(raw)
    if isinstance(raw, str):
        return raw.encode("latin-1", errors="ignore")
    if isinstance(raw, BytesIO):
        return raw.getvalue()
    return bytes(raw)
