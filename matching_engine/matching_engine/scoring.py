"""Scoring calculations and weighted aggregation."""

from __future__ import annotations

from matching_engine.config import WEIGHTS


def calculate_overall_score(
    skill_score: float,
    experience_score: float,
    education_score: float,
    text_similarity_score: float,
) -> float:
    """
    Calculate the weighted total overall match score from component scores.
    Uses strictly the WEIGHTS dict defined in config.py.
    """
    total = (
        (WEIGHTS["skills"] * skill_score)
        + (WEIGHTS["experience"] * experience_score)
        + (WEIGHTS["education"] * education_score)
        + (WEIGHTS["text"] * text_similarity_score)
    )
    clamped = max(0.0, min(100.0, total))
    return round(clamped, 2)
