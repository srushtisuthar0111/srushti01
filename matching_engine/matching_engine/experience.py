"""Experience parsing and evaluation logic."""

from __future__ import annotations

import re
from typing import Any

from matching_engine.models import CandidateProfile, JobProfile

_MONTHS = {
    "jan": 1, "january": 1,
    "feb": 2, "february": 2,
    "mar": 3, "march": 3,
    "apr": 4, "april": 4,
    "may": 5,
    "jun": 6, "june": 6,
    "jul": 7, "july": 7,
    "aug": 8, "august": 8,
    "sep": 9, "september": 9,
    "oct": 10, "october": 10,
    "nov": 11, "november": 11,
    "dec": 12, "december": 12,
}

_CURRENT_YEAR = 2026


def _parse_month_year(text: str) -> tuple[int, int] | None:
    """Parse month and year from a fragment like 'Jan 2021' or '2021'."""
    text = text.strip().lower()
    if text in ("present", "current", "now"):
        return _CURRENT_YEAR, 9  # Current period

    # Check for Month Year
    m = re.search(r"([a-z]+)\.?\s+(\d{4})", text)
    if m:
        month_str = m.group(1).lower()
        year = int(m.group(2))
        month = _MONTHS.get(month_str, 1)
        return year, month

    # Check for Year only
    m_year = re.search(r"(\d{4})", text)
    if m_year:
        return int(m_year.group(1)), 1

    return None


def _parse_date_range_years(text: str) -> float:
    """Parse duration in years from date range like 'Jan 2021 - Mar 2023' or '2019-2022'."""
    pattern = r"([a-z\.]+\s+\d{4}|\d{4})\s*(?:-|to|–)\s*([a-z\.]+\s+\d{4}|\d{4}|present|current|now)"
    match = re.search(pattern, text, re.IGNORECASE)
    if match:
        start_pt = _parse_month_year(match.group(1))
        end_pt = _parse_month_year(match.group(2))
        if start_pt and end_pt:
            start_yr, start_mo = start_pt
            end_yr, end_mo = end_pt
            diff_years = (end_yr - start_yr) + (end_mo - start_mo) / 12.0
            return max(0.0, round(diff_years, 2))
    return 0.0


def _parse_single_experience_entry(entry: Any) -> float:
    """Extract years of experience from a single string or dict entry."""
    if entry is None:
        return 0.0

    # Dict entry handler
    if isinstance(entry, dict):
        # 1. Direct 'years' key
        if "years" in entry and entry["years"] is not None:
            try:
                return max(0.0, float(re.findall(r"\d+(?:\.\d+)?", str(entry["years"]))[0]))
            except (IndexError, ValueError):
                pass

        # 2. 'duration' key
        if "duration" in entry and entry["duration"]:
            years = _parse_single_experience_entry(str(entry["duration"]))
            if years > 0:
                return years

        # 3. 'start' and 'end' keys
        start_val = str(entry.get("start") or "").strip()
        end_val = str(entry.get("end") or "").strip()
        if start_val and end_val:
            range_str = f"{start_val} - {end_val}"
            years = _parse_date_range_years(range_str)
            if years > 0:
                return years

        # Fallback to inspecting all text values in dict
        combined = " ".join(str(v) for v in entry.values() if v)
        return _parse_single_experience_entry(combined)

    # String entry handler
    text = str(entry).strip()
    if not text:
        return 0.0

    # Pattern: '2 years', '3.5 yrs', '5+ years'
    m_years = re.search(r"(\d+(?:\.\d+)?)\s*\+?\s*(?:years?|yrs?)", text, re.IGNORECASE)
    if m_years:
        try:
            return float(m_years.group(1))
        except ValueError:
            pass

    # Pattern: '18 months', '6 mos'
    m_months = re.search(r"(\d+(?:\.\d+)?)\s*(?:months?|mos?)", text, re.IGNORECASE)
    if m_months:
        try:
            return round(float(m_months.group(1)) / 12.0, 2)
        except ValueError:
            pass

    # Pattern: Date range like 'Jan 2021 - Mar 2023' or '2019 - 2022'
    date_years = _parse_date_range_years(text)
    if date_years > 0:
        return date_years

    return 0.0


def extract_candidate_years(experience_entries: list[Any]) -> float:
    """Extract total years of experience across all candidate experience entries."""
    if not experience_entries:
        return 0.0
    total = 0.0
    for entry in experience_entries:
        total += _parse_single_experience_entry(entry)
    return round(total, 2)


def extract_job_required_years(experience_entries: list[Any]) -> float:
    """Extract required years of experience from job profile (using minimum if range)."""
    if not experience_entries:
        return 0.0

    text_parts = []
    for entry in experience_entries:
        if isinstance(entry, dict):
            if "years" in entry and entry["years"] is not None:
                try:
                    return float(re.findall(r"\d+(?:\.\d+)?", str(entry["years"]))[0])
                except (IndexError, ValueError):
                    pass
            text_parts.extend(str(v) for v in entry.values() if v)
        elif entry is not None:
            text_parts.append(str(entry))

    combined = " ".join(text_parts)

    # Range check e.g. '2-4 years' or '2 to 5 years' -> use minimum
    m_range = re.search(r"(\d+(?:\.\d+)?)\s*(?:-|to|–)\s*(\d+(?:\.\d+)?)\s*(?:years?|yrs?)", combined, re.IGNORECASE)
    if m_range:
        try:
            val1 = float(m_range.group(1))
            val2 = float(m_range.group(2))
            return min(val1, val2)
        except ValueError:
            pass

    # Standard requirement e.g. '3+ years', '3 years'
    m_single = re.search(r"(\d+(?:\.\d+)?)\+?\s*(?:years?|yrs?)", combined, re.IGNORECASE)
    if m_single:
        try:
            return float(m_single.group(1))
        except ValueError:
            pass

    return 0.0


def evaluate_experience(candidate: CandidateProfile, job: JobProfile) -> tuple[float, str]:
    """
    Evaluate candidate experience against job requirements.
    
    Returns:
        (experience_score, experience_result)
    """
    candidate_years = extract_candidate_years(candidate.experience)
    required_years = extract_job_required_years(job.experience)

    if required_years <= 0.0:
        return 100.0, "No experience requirement specified"

    ratio = candidate_years / required_years

    if ratio >= 1.0:
        score = 100.0
        result_text = "Requirement satisfied"
    elif ratio >= 0.75:
        score = min(100.0, ratio * 100.0)
        result_text = "Close to requirement"
    elif ratio >= 0.5:
        score = min(100.0, ratio * 100.0)
        result_text = "Partially meets requirement"
    else:
        score = min(100.0, ratio * 100.0)
        result_text = "Below requirement"

    return round(score, 2), result_text
