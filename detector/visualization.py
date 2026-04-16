from __future__ import annotations

from html import escape
from typing import Iterable

import pandas as pd


def _risk_color(score: float) -> str:
    if score >= 0.75:
        return "#D64545"  # red
    if score >= 0.45:
        return "#F4A300"  # yellow
    return "#2E8B57"  # green


def build_heatmap_html(df: pd.DataFrame) -> str:
    blocks = []
    for _, row in df.iterrows():
        color = _risk_color(float(row["risk_score"]))
        para = escape(str(row["paragraph"]))
        blocks.append(
            f"""
            <div style=\"border-left: 8px solid {color}; background:#FAFAFA; padding: 12px; margin: 10px 0; border-radius: 8px;\">
                <div style=\"font-size: 12px; color: #444; margin-bottom: 6px;\">Paragraph {int(row['paragraph_index'])}</div>
                <div style=\"font-size: 14px; line-height: 1.5; color:#1F1F1F;\">{para}</div>
                <div style=\"margin-top: 8px; font-size: 12px; color:#333;\">
                    Plagiarism: <b>{row['plagiarism_score']:.2f}</b> | AI: <b>{row['ai_probability']:.2f}</b> | Combined Risk: <b>{row['risk_score']:.2f}</b>
                </div>
            </div>
            """
        )

    return "\n".join(blocks)


def summarize_metrics(df: pd.DataFrame) -> dict:
    return {
        "paragraph_count": int(len(df)),
        "avg_plagiarism": float(df["plagiarism_score"].mean()) if len(df) else 0.0,
        "avg_ai_probability": float(df["ai_probability"].mean()) if len(df) else 0.0,
        "high_risk_sections": int((df["risk_score"] >= 0.75).sum()) if len(df) else 0,
    }


def top_suspicious_rows(df: pd.DataFrame, top_k: int = 5) -> pd.DataFrame:
    if df.empty:
        return df
    return df.sort_values(by="risk_score", ascending=False).head(top_k).copy()
