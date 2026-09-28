"""Main matching engine coordinator."""

from __future__ import annotations

from typing import Any

from matching_engine.education import evaluate_education
from matching_engine.experience import evaluate_experience
from matching_engine.explain import get_recommendation
from matching_engine.models import CandidateProfile, JobProfile, MatchResult
from matching_engine.scoring import calculate_overall_score
from matching_engine.skills import evaluate_skills
from matching_engine.text_similarity import compute_text_similarity


def _flatten_items(items: Any) -> str:
    """Helper to extract flat text from string/dict items or nested iterables."""
    if items is None:
        return ""
    if isinstance(items, str):
        return items
    if not isinstance(items, (list, tuple, set)):
        return str(items)
    parts: list[str] = []
    for item in items:
        if isinstance(item, dict):
            parts.extend(str(v) for v in item.values() if v is not None)
        elif isinstance(item, (list, tuple, set)):
            parts.append(_flatten_items(item))
        elif item is not None:
            parts.append(str(item))
    return " ".join(parts)


def match(
    candidate: CandidateProfile | dict[str, Any] | None,
    job: JobProfile | dict[str, Any] | None,
) -> MatchResult:
    """
    Match a candidate profile against a job profile.
    Accepts CandidateProfile/JobProfile instances or raw dictionaries.
    Tolerates missing fields and incorrect types.
    Always returns a MatchResult instance.
    """
    cand = CandidateProfile.from_dict(candidate)
    jp = JobProfile.from_dict(job)

    # 1. Skills evaluation
    skill_score, matched_req, missing_req, matched_pref = evaluate_skills(cand, jp)

    # 2. Experience evaluation
    exp_score, exp_result = evaluate_experience(cand, jp)

    # 3. Education evaluation
    edu_score, edu_result = evaluate_education(cand, jp)

    # 4. Text similarity evaluation
    # Candidate text = skills + projects + experience text
    cand_text_components = [
        " ".join(str(s) for s in cand.skills if s is not None),
        _flatten_items(cand.projects),
        _flatten_items(cand.experience),
    ]
    cand_text = " ".join(p for p in cand_text_components if p.strip())

    # Job text = title + description + skills
    job_text_components = [
        str(jp.title or ""),
        str(jp.description or ""),
        " ".join(str(s) for s in jp.required_skills if s is not None),
        " ".join(str(s) for s in jp.preferred_skills if s is not None),
    ]
    job_text = " ".join(p for p in job_text_components if p.strip())

    text_score = compute_text_similarity(cand_text, job_text)

    # 5. Overall weighted score
    overall_score = calculate_overall_score(
        skill_score=skill_score,
        experience_score=exp_score,
        education_score=edu_score,
        text_similarity_score=text_score,
    )

    # 6. Recommendation tier
    recommendation = get_recommendation(overall_score)

    return MatchResult(
        overall_score=overall_score,
        skill_score=skill_score,
        experience_score=exp_score,
        education_score=edu_score,
        text_similarity_score=text_score,
        matched_required_skills=matched_req,
        missing_required_skills=missing_req,
        matched_preferred_skills=matched_pref,
        education_result=edu_result,
        experience_result=exp_result,
        recommendation=recommendation,
    )
