"""Education evaluation logic based on level hierarchy."""

from __future__ import annotations

import re
from typing import Any

from matching_engine.config import EDUCATION_ALIASES, EDUCATION_LEVELS
from matching_engine.models import CandidateProfile, JobProfile


def _detect_all_education_levels(entry: Any) -> list[int]:
    """Detect all education level integers (1-5) mentioned in an entry."""
    if entry is None:
        return []

    text = ""
    if isinstance(entry, dict):
        text = " ".join(str(v) for v in entry.values() if v)
    else:
        text = str(entry)

    text = text.lower().strip()
    if not text:
        return []

    detected_levels: list[int] = []
    matched_spans: list[tuple[int, int]] = []

    # Sort aliases by word length descending so multi-word aliases match before single-word
    sorted_aliases = sorted(EDUCATION_ALIASES.items(), key=lambda kv: len(kv[0]), reverse=True)

    for alias, canonical in sorted_aliases:
        pattern = r"(?<![a-zA-Z0-9])" + re.escape(alias) + r"(?![a-zA-Z0-9])"
        for match in re.finditer(pattern, text):
            span = match.span()
            if not any(s <= span[0] and span[1] <= e for s, e in matched_spans):
                matched_spans.append(span)
                level_num = EDUCATION_LEVELS.get(canonical, 0)
                if level_num > 0 and level_num not in detected_levels:
                    detected_levels.append(level_num)

    return detected_levels


def _detect_education_level(entry: Any) -> int:
    """Detect the highest education level integer (1-5) from an entry."""
    levels = _detect_all_education_levels(entry)
    return max(levels) if levels else 0


def detect_candidate_highest_education(education_entries: list[Any]) -> int:
    """Detect the candidate's highest education level."""
    if not education_entries:
        return 0
    all_levels = []
    for entry in education_entries:
        all_levels.extend(_detect_all_education_levels(entry))
    return max(all_levels) if all_levels else 0


def detect_job_required_education(education_entries: list[Any]) -> int:
    """Detect the job's minimum required education level."""
    if not education_entries:
        return 0
    all_levels = []
    for entry in education_entries:
        all_levels.extend(_detect_all_education_levels(entry))
    return min(all_levels) if all_levels else 0


def evaluate_education(candidate: CandidateProfile, job: JobProfile) -> tuple[float, str]:
    """
    Evaluate candidate education against job requirements.
    
    Returns:
        (education_score, education_result)
    """
    cand_level = detect_candidate_highest_education(candidate.education)
    job_level = detect_job_required_education(job.education)

    # If job specifies no education requirement
    if job_level == 0:
        return 100.0, "No education requirement specified"

    # If candidate education is missing or unrecognized
    if cand_level == 0:
        return 0.0, "Candidate education not specified or detected"

    # Candidate meets or exceeds requirement
    if cand_level >= job_level:
        return 100.0, "Requirement satisfied"

    # One level below
    if cand_level == job_level - 1:
        return 60.0, "Slightly below requirement"

    # Two or more levels below
    return 30.0, "Significantly below requirement"
