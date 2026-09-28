"""Tests validating strict compliance with the shared data contract in Section 3 and 10."""

from matching_engine.config import DISCLAIMER
from matching_engine.engine import match
from matching_engine.explain import explain
from matching_engine.models import CandidateProfile, JobProfile, MatchResult
from tests.fixtures import SENIOR_DEV_CANDIDATE, STANDARD_JOB


def test_candidate_profile_contract_keys():
    cand = CandidateProfile(
        name="John Doe",
        email="john@example.com",
        skills=["Python"],
        education=["Bachelor of Science"],
        experience=["3 years"],
        projects=["Project X"],
    )
    d = cand.to_dict()
    expected_keys = {"name", "email", "skills", "education", "experience", "projects"}
    assert set(d.keys()) == expected_keys
    assert isinstance(d["name"], str)
    assert isinstance(d["email"], str)
    assert isinstance(d["skills"], list)
    assert isinstance(d["education"], list)
    assert isinstance(d["experience"], list)
    assert isinstance(d["projects"], list)


def test_job_profile_contract_keys():
    job = JobProfile(
        title="Software Engineer",
        required_skills=["Python"],
        preferred_skills=["Docker"],
        education=["Bachelor"],
        experience=["2 years"],
        description="Write clean code.",
    )
    d = job.to_dict()
    expected_keys = {
        "title",
        "required_skills",
        "preferred_skills",
        "education",
        "experience",
        "description",
    }
    assert set(d.keys()) == expected_keys
    assert isinstance(d["title"], str)
    assert isinstance(d["required_skills"], list)
    assert isinstance(d["preferred_skills"], list)
    assert isinstance(d["education"], list)
    assert isinstance(d["experience"], list)
    assert isinstance(d["description"], str)


def test_match_result_contract_keys_and_types():
    result = match(SENIOR_DEV_CANDIDATE, STANDARD_JOB)
    d = result.to_dict()

    expected_keys = {
        "overall_score",
        "skill_score",
        "experience_score",
        "education_score",
        "text_similarity_score",
        "matched_required_skills",
        "missing_required_skills",
        "matched_preferred_skills",
        "education_result",
        "experience_result",
        "recommendation",
    }
    assert set(d.keys()) == expected_keys

    # Check value types
    assert isinstance(d["overall_score"], float)
    assert isinstance(d["skill_score"], float)
    assert isinstance(d["experience_score"], float)
    assert isinstance(d["education_score"], float)
    assert isinstance(d["text_similarity_score"], float)
    assert isinstance(d["matched_required_skills"], list)
    assert isinstance(d["missing_required_skills"], list)
    assert isinstance(d["matched_preferred_skills"], list)
    assert isinstance(d["education_result"], str)
    assert isinstance(d["experience_result"], str)
    assert isinstance(d["recommendation"], str)


def test_match_result_floats_are_rounded():
    result = match(SENIOR_DEV_CANDIDATE, STANDARD_JOB)
    d = result.to_dict()
    for key in ["overall_score", "skill_score", "experience_score", "education_score", "text_similarity_score"]:
        val = d[key]
        # Should have at most 2 decimal digits
        assert val == round(val, 2)


def test_mandatory_disclaimer_present_in_explanation():
    result = match(SENIOR_DEV_CANDIDATE, STANDARD_JOB)
    report = explain(result)
    assert DISCLAIMER in report
    assert "Recruiters remain responsible for all final hiring decisions." in report


def test_dict_and_dataclass_input_parity():
    # Calling with dataclasses
    cand_obj = CandidateProfile.from_dict(SENIOR_DEV_CANDIDATE)
    job_obj = JobProfile.from_dict(STANDARD_JOB)
    res_obj = match(cand_obj, job_obj)

    # Calling with plain dictionaries
    res_dict = match(SENIOR_DEV_CANDIDATE, STANDARD_JOB)

    assert res_obj.to_dict() == res_dict.to_dict()
