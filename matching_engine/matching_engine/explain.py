"""Explanation generator and recommendation tier resolver."""

from __future__ import annotations

from typing import Any

from matching_engine.config import DISCLAIMER, RECOMMENDATION_TIERS
from matching_engine.models import MatchResult


def get_recommendation(score: float) -> str:
    """Determine recommendation tier based on overall score."""
    for threshold, tier_text in RECOMMENDATION_TIERS:
        if score >= threshold:
            return tier_text
    return RECOMMENDATION_TIERS[-1][1]


def explain(result: MatchResult | dict[str, Any]) -> str:
    """
    Build a comprehensive, human-readable explanation of match results.
    Adheres strictly to decision-support terminology (no hire/reject directives)
    and concludes with the mandatory platform disclaimer.
    """
    if isinstance(result, MatchResult):
        data = result.to_dict()
    elif isinstance(result, dict):
        data = result
    else:
        raise TypeError("result must be a MatchResult instance or dictionary")

    overall = data.get("overall_score", 0.0)
    skill = data.get("skill_score", 0.0)
    exp = data.get("experience_score", 0.0)
    edu = data.get("education_score", 0.0)
    text_sim = data.get("text_similarity_score", 0.0)

    matched_req = data.get("matched_required_skills", [])
    missing_req = data.get("missing_required_skills", [])
    matched_pref = data.get("matched_preferred_skills", [])
    exp_res = data.get("experience_result", "")
    edu_res = data.get("education_result", "")
    recommendation = data.get("recommendation", get_recommendation(overall))

    lines = [
        "============================================================",
        "             AI RESUME-JOB MATCH EVALUATION REPORT          ",
        "============================================================",
        f"Overall Match Score: {overall:.2f}/100",
        f"Recommendation: {recommendation}",
        "",
        "COMPONENT BREAKDOWN:",
        f"- Skills Score: {skill:.2f}/100",
        f"  * Matched Required Skills ({len(matched_req)}): {', '.join(matched_req) if matched_req else 'None'}",
        f"  * Missing Required Skills ({len(missing_req)}): {', '.join(missing_req) if missing_req else 'None'}",
        f"  * Matched Preferred Skills ({len(matched_pref)}): {', '.join(matched_pref) if matched_pref else 'None'}",
        f"- Experience Score: {exp:.2f}/100 ({exp_res})",
        f"- Education Score: {edu:.2f}/100 ({edu_res})",
        f"- Text Alignment Score: {text_sim:.2f}/100",
        "============================================================",
        DISCLAIMER,
    ]
    return "\n".join(lines)
