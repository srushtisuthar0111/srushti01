"""Skill evaluation and matching logic."""

from __future__ import annotations

import re
from typing import Any

from matching_engine.config import DEFAULT_NEUTRAL_SKILL_SCORE, SKILL_ALIASES
from matching_engine.models import CandidateProfile, JobProfile
from matching_engine.normalizer import normalize_skill


def _extract_all_text(items: list[Any]) -> str:
    """Extract flat text from list of strings or dictionaries."""
    parts: list[str] = []
    for item in items:
        if isinstance(item, dict):
            for v in item.values():
                if v:
                    parts.append(str(v))
        elif isinstance(item, (list, tuple)):
            parts.append(_extract_all_text(list(item)))
        elif item is not None:
            parts.append(str(item))
    return " ".join(parts)


def _skill_in_text(term: str, text: str) -> bool:
    """Check if a term appears as an isolated token in text."""
    if not term or not text:
        return False
    # Boundary check that respects non-alphanumeric symbols in tech terms (e.g. c++, c#, .net)
    pattern = r"(?<![a-zA-Z0-9])" + re.escape(term) + r"(?![a-zA-Z0-9])"
    return bool(re.search(pattern, text, re.IGNORECASE))


def _build_alias_lookup() -> dict[str, set[str]]:
    """Build reverse mapping of canonical skill to known aliases."""
    reverse: dict[str, set[str]] = {}
    for alias, canonical in SKILL_ALIASES.items():
        reverse.setdefault(canonical, set()).add(alias)
    return reverse


_REVERSE_ALIASES = _build_alias_lookup()


def _is_skill_present(
    job_skill: str,
    candidate_skills_norm: set[str],
    candidate_body_text: str,
) -> bool:
    """Check if a job skill is matched in candidate's skills list or project/experience text."""
    raw_lower = job_skill.lower().strip()
    norm_skill = normalize_skill(job_skill)

    # 1. Direct match in candidate's declared skills
    if norm_skill in candidate_skills_norm or raw_lower in candidate_skills_norm:
        return True

    # Check known aliases against candidate declared skills
    for alias in _REVERSE_ALIASES.get(norm_skill, set()):
        if alias in candidate_skills_norm:
            return True

    # 2. Check candidate projects and experience text (documented feature)
    # Search for canonical term, raw job skill term, and known aliases
    terms_to_check = {norm_skill, raw_lower} | _REVERSE_ALIASES.get(norm_skill, set())
    for term in terms_to_check:
        if term and _skill_in_text(term, candidate_body_text):
            return True

    return False


def evaluate_skills(
    candidate: CandidateProfile,
    job: JobProfile,
) -> tuple[float, list[str], list[str], list[str]]:
    """
    Evaluate candidate skills against job requirements.
    
    Returns:
        (skill_score, matched_required_skills, missing_required_skills, matched_preferred_skills)
    """
    # Normalize candidate declared skills
    candidate_skills_norm = {normalize_skill(s) for s in candidate.skills if normalize_skill(s)}
    # Include raw lowercase skills as well for resilience
    candidate_skills_norm.update(s.lower().strip() for s in candidate.skills if str(s).strip())

    # Extract text from candidate projects and experience for contextual matching
    cand_body_text = _extract_all_text(candidate.projects) + " " + _extract_all_text(candidate.experience)

    matched_required: list[str] = []
    missing_required: list[str] = []
    for req in job.required_skills:
        if _is_skill_present(req, candidate_skills_norm, cand_body_text):
            matched_required.append(req)
        else:
            missing_required.append(req)

    matched_preferred: list[str] = []
    for pref in job.preferred_skills:
        if _is_skill_present(pref, candidate_skills_norm, cand_body_text):
            matched_preferred.append(pref)

    total_req = len(job.required_skills)
    total_pref = len(job.preferred_skills)
    matched_req_count = len(matched_required)
    matched_pref_count = len(matched_preferred)

    if total_req > 0 and total_pref > 0:
        score = (80.0 * (matched_req_count / total_req)) + (20.0 * (matched_pref_count / total_pref))
    elif total_req > 0:
        score = 100.0 * (matched_req_count / total_req)
    elif total_pref > 0:
        score = 100.0 * (matched_pref_count / total_pref)
    else:
        score = DEFAULT_NEUTRAL_SKILL_SCORE

    clamped_score = max(0.0, min(100.0, round(score, 2)))
    return clamped_score, matched_required, missing_required, matched_preferred
