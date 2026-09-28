"""Tests for experience parsing and evaluation logic."""

from matching_engine.experience import (
    evaluate_experience,
    extract_candidate_years,
    extract_job_required_years,
)
from matching_engine.models import CandidateProfile, JobProfile


def test_experience_bands():
    job = JobProfile(experience=["4 years"])

    # Band 1: ratio >= 1.0 -> 100 "Requirement satisfied"
    cand_100 = CandidateProfile(experience=["5 years"])
    score_100, res_100 = evaluate_experience(cand_100, job)
    assert score_100 == 100.0
    assert res_100 == "Requirement satisfied"

    # Band 2: 0.75 <= ratio < 1.0 -> 75% -> "Close to requirement"
    cand_75 = CandidateProfile(experience=["3 years"])
    score_75, res_75 = evaluate_experience(cand_75, job)
    assert score_75 == 75.0
    assert res_75 == "Close to requirement"

    # Band 3: 0.5 <= ratio < 0.75 -> 50% -> "Partially meets requirement"
    cand_50 = CandidateProfile(experience=["2 years"])
    score_50, res_50 = evaluate_experience(cand_50, job)
    assert score_50 == 50.0
    assert res_50 == "Partially meets requirement"

    # Band 4: ratio < 0.5 -> 25% -> "Below requirement"
    cand_25 = CandidateProfile(experience=["1 year"])
    score_25, res_25 = evaluate_experience(cand_25, job)
    assert score_25 == 25.0
    assert res_25 == "Below requirement"


def test_tolerant_candidate_parsing():
    # String with explicit years
    assert extract_candidate_years(["2 years at Company A", "3.5 yrs at Company B"]) == 5.5

    # Dicts with years / duration / start & end
    entries = [
        {"years": 2},
        {"duration": "18 months"},
        {"start": "2020", "end": "2022"},
    ]
    years = extract_candidate_years(entries)
    # 2 + 1.5 + 2 = 5.5
    assert years == 5.5

    # Date range in string
    assert extract_candidate_years(["Jan 2021 - Mar 2023"]) > 2.0


def test_job_required_years_range_minimum():
    # '2-4 years' -> takes minimum 2
    assert extract_job_required_years(["2-4 years of experience"]) == 2.0
    assert extract_job_required_years(["3+ years"]) == 3.0
    assert extract_job_required_years([{"years": 5}]) == 5.0


def test_no_experience_requirement():
    cand = CandidateProfile(experience=["1 year"])
    job_empty = JobProfile(experience=[])
    score, msg = evaluate_experience(cand, job_empty)
    assert score == 100.0
    assert msg == "No experience requirement specified"


def test_malformed_and_empty_experience_never_crash():
    cand_corrupted = CandidateProfile(experience=[None, {}, "no numbers here", 12345])
    job = JobProfile(experience=["3 years"])
    score, msg = evaluate_experience(cand_corrupted, job)
    assert score == 0.0
    assert msg == "Below requirement"
