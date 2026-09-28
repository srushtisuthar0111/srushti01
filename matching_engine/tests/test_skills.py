"""Tests for skills normalization and matching logic."""

from matching_engine.models import CandidateProfile, JobProfile
from matching_engine.normalizer import normalize_skill, normalize_skills
from matching_engine.skills import evaluate_skills


def test_normalize_skill_aliases():
    assert normalize_skill("js") == "javascript"
    assert normalize_skill("py") == "python"
    assert normalize_skill("postgres") == "postgresql"
    assert normalize_skill("reactjs") == "react"
    assert normalize_skill("react.js") == "react"
    assert normalize_skill("node") == "node.js"
    assert normalize_skill("nodejs") == "node.js"
    assert normalize_skill("ml") == "machine learning"
    assert normalize_skill("  PYTHON  ") == "python"


def test_normalize_skills_dedupe():
    skills = ["Python", "python", "py", "JS", "javascript", "Docker"]
    normalized = normalize_skills(skills)
    assert normalized == ["python", "javascript", "docker"]


def test_exact_and_case_skill_match():
    candidate = CandidateProfile(skills=["python", "postgresql", "docker"])
    job = JobProfile(required_skills=["Python", "PostgreSQL"], preferred_skills=["Docker"])
    score, matched_req, missing_req, matched_pref = evaluate_skills(candidate, job)

    assert score == 100.0
    # Original job-side spelling preserved
    assert matched_req == ["Python", "PostgreSQL"]
    assert missing_req == []
    assert matched_pref == ["Docker"]


def test_alias_matching():
    candidate = CandidateProfile(skills=["py", "postgres", "js"])
    job = JobProfile(required_skills=["Python", "PostgreSQL", "JavaScript"])
    score, matched_req, missing_req, _ = evaluate_skills(candidate, job)

    assert score == 100.0
    assert matched_req == ["Python", "PostgreSQL", "JavaScript"]
    assert missing_req == []


def test_all_matched_and_none_matched():
    cand_none = CandidateProfile(skills=["Ruby", "Rails"])
    job = JobProfile(required_skills=["Python", "Go"])
    score_none, matched_none, missing_none, _ = evaluate_skills(cand_none, job)
    assert score_none == 0.0
    assert matched_none == []
    assert missing_none == ["Python", "Go"]

    cand_all = CandidateProfile(skills=["Python", "Go"])
    score_all, matched_all, missing_all, _ = evaluate_skills(cand_all, job)
    assert score_all == 100.0
    assert matched_all == ["Python", "Go"]
    assert missing_all == []


def test_required_vs_preferred_penalty_difference():
    # Case A: Missing 1 of 2 required skills (has all preferred)
    cand_a = CandidateProfile(skills=["Python", "AWS"])
    job_a = JobProfile(required_skills=["Python", "Docker"], preferred_skills=["AWS"])
    score_a, matched_req_a, missing_req_a, matched_pref_a = evaluate_skills(cand_a, job_a)
    # 80% * (1/2) + 20% * (1/1) = 40 + 20 = 60.0
    assert score_a == 60.0

    # Case B: Has all required skills, missing preferred skill
    cand_b = CandidateProfile(skills=["Python", "Docker"])
    job_b = JobProfile(required_skills=["Python", "Docker"], preferred_skills=["AWS"])
    score_b, matched_req_b, missing_req_b, matched_pref_b = evaluate_skills(cand_b, job_b)
    # 80% * (2/2) + 20% * (0/1) = 80 + 0 = 80.0
    # Missing preferred only loses the 20% bonus, not heavily penalized
    assert score_b == 80.0
    assert score_b > score_a


def test_empty_skills_neutral_score():
    cand = CandidateProfile(skills=[])
    job = JobProfile(required_skills=[], preferred_skills=[])
    score, matched_req, missing_req, matched_pref = evaluate_skills(cand, job)
    assert score == 50.0
    assert matched_req == []
    assert missing_req == []
    assert matched_pref == []


def test_skill_mentions_in_project_and_experience_text():
    cand = CandidateProfile(
        skills=[],
        projects=[{"description": "Developed backend microservices using Python and Docker."}],
        experience=["Worked with PostgreSQL databases and AWS services."],
    )
    job = JobProfile(required_skills=["Python", "PostgreSQL"], preferred_skills=["Docker", "AWS"])
    score, matched_req, missing_req, matched_pref = evaluate_skills(cand, job)
    assert score == 100.0
    assert matched_req == ["Python", "PostgreSQL"]
    assert missing_req == []
    assert matched_pref == ["Docker", "AWS"]


def test_whole_word_matching_boundary():
    # Ensure substring like 'c' doesn't match 'css', or 'java' doesn't match 'javascript'
    cand = CandidateProfile(skills=["javascript"])
    job = JobProfile(required_skills=["Java"])
    score, matched_req, missing_req, _ = evaluate_skills(cand, job)
    assert score == 0.0
    assert missing_req == ["Java"]
