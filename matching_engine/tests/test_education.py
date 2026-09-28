"""Tests for education evaluation and degree hierarchy logic."""

from matching_engine.education import (
    _detect_all_education_levels,
    _detect_education_level,
    detect_candidate_highest_education,
    detect_job_required_education,
    evaluate_education,
)
from matching_engine.models import CandidateProfile, JobProfile


def test_detect_education_level_basic():
    assert _detect_education_level("High School Diploma") == 1
    assert _detect_education_level("Polytechnic Diploma in Mechanical") == 2
    assert _detect_education_level("Bachelor of Science in Computer Science") == 3
    assert _detect_education_level("Master of Science in Artificial Intelligence") == 4
    assert _detect_education_level("PhD in Computer Engineering") == 5


def test_detect_education_aliases():
    # Bachelor aliases
    for term in ["B.Tech", "btech", "B.E.", "be", "B.Sc", "bsc", "BS", "b.s.", "BCA", "BBA"]:
        assert _detect_education_level(f"Degree in {term}") == 3

    # Master aliases
    for term in ["M.Tech", "mtech", "M.E.", "me", "M.Sc", "msc", "MS", "m.s.", "MCA", "MBA"]:
        assert _detect_education_level(f"Degree in {term}") == 4

    # High School aliases
    for term in ["10th", "12th", "Secondary", "Higher Secondary", "GED", "HSC", "SSC"]:
        assert _detect_education_level(f"Completed {term}") == 1

    # PhD aliases
    for term in ["Ph.D.", "phd", "Doctorate", "Doctoral"]:
        assert _detect_education_level(f"{term} in Machine Learning") == 5


def test_candidate_meets_exact_requirement():
    cand = CandidateProfile(education=["Bachelor of Science in CS"])
    job = JobProfile(education=["Bachelor degree in Computer Science"])
    score, res = evaluate_education(cand, job)
    assert score == 100.0
    assert res == "Requirement satisfied"


def test_candidate_exceeds_requirement():
    cand = CandidateProfile(education=["Master of Technology in Software Systems"])
    job = JobProfile(education=["Bachelor degree"])
    score, res = evaluate_education(cand, job)
    assert score == 100.0
    assert res == "Requirement satisfied"


def test_candidate_one_level_below():
    cand = CandidateProfile(education=["Diploma in Computer Application"])
    job = JobProfile(education=["Bachelor of Science"])
    score, res = evaluate_education(cand, job)
    assert score == 60.0
    assert res == "Slightly below requirement"


def test_candidate_two_levels_below():
    cand = CandidateProfile(education=["High School Diploma"])
    job = JobProfile(education=["Bachelor of Technology"])
    score, res = evaluate_education(cand, job)
    assert score == 30.0
    assert res == "Significantly below requirement"


def test_job_no_education_requirement():
    cand = CandidateProfile(education=["High School Diploma"])
    job = JobProfile(education=[])
    score, res = evaluate_education(cand, job)
    assert score == 100.0
    assert res == "No education requirement specified"


def test_candidate_missing_education():
    cand = CandidateProfile(education=[])
    job = JobProfile(education=["Bachelor degree"])
    score, res = evaluate_education(cand, job)
    assert score == 0.0
    assert res == "Candidate education not specified or detected"


def test_dict_education_entries():
    cand = CandidateProfile(
        education=[{"degree": "Bachelor of Technology", "institution": "State University"}]
    )
    job = JobProfile(education=[{"requirement": "B.Tech or equivalent"}])
    score, res = evaluate_education(cand, job)
    assert score == 100.0
    assert res == "Requirement satisfied"


def test_multiple_education_entries_highest_selected():
    cand = CandidateProfile(
        education=[
            "High School (12th Grade)",
            "Diploma in Engineering",
            "B.Tech in Computer Science",
            "Master of Science in Data Science",
        ]
    )
    highest = detect_candidate_highest_education(cand.education)
    assert highest == 4  # Master


def test_job_multiple_entries_minimum_required():
    job = JobProfile(education=["Diploma", "Bachelor degree"])
    min_req = detect_job_required_education(job.education)
    assert min_req == 2  # Diploma is acceptable


def test_job_single_string_multiple_options():
    job = JobProfile(education=["Diploma or Bachelor required"])
    min_req = detect_job_required_education(job.education)
    assert min_req == 2


def test_corrupted_education_data():
    cand = CandidateProfile(education=[None, {}, 12345, "unrelated text without degree"])
    job = JobProfile(education=["Bachelor"])
    score, res = evaluate_education(cand, job)
    assert score == 0.0
    assert res == "Candidate education not specified or detected"
