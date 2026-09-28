"""End-to-end integration tests using mock profile fixtures."""

from matching_engine.engine import match
from matching_engine.models import MatchResult
from tests.fixtures import (
    ALIAS_CANDIDATE,
    EMPTY_CANDIDATE,
    ENTRY_JOB,
    JUNIOR_DEV_CANDIDATE,
    NO_REQUIREMENTS_JOB,
    PROJECT_SKILL_CANDIDATE,
    SELF_TAUGHT_CANDIDATE,
    SENIOR_DEV_CANDIDATE,
    STANDARD_JOB,
)


def test_senior_candidate_on_standard_job():
    result = match(SENIOR_DEV_CANDIDATE, STANDARD_JOB)
    assert isinstance(result, MatchResult)
    # Senior meets all required skills (Python, PostgreSQL, Docker)
    assert set(result.matched_required_skills) == {"Python", "PostgreSQL", "Docker"}
    assert result.missing_required_skills == []
    # Has AWS preferred skill
    assert "AWS" in result.matched_preferred_skills
    # 5 years vs 3+ years
    assert result.experience_score == 100.0
    assert result.experience_result == "Requirement satisfied"
    # B.Tech meets Bachelor
    assert result.education_score == 100.0
    assert result.education_result == "Requirement satisfied"
    # Overall score should be strong match (>= 80)
    assert result.overall_score >= 80.0
    assert "Strong match" in result.recommendation


def test_junior_candidate_on_standard_job():
    result = match(JUNIOR_DEV_CANDIDATE, STANDARD_JOB)
    assert isinstance(result, MatchResult)
    # Junior is missing PostgreSQL and Docker
    assert "Python" in result.matched_required_skills
    assert "PostgreSQL" in result.missing_required_skills
    assert "Docker" in result.missing_required_skills
    # 1 year vs 3+ years -> 33.33%
    assert result.experience_score < 50.0
    assert result.experience_result == "Below requirement"
    # High School vs Bachelor -> 2 levels below (30.0%)
    assert result.education_score == 30.0
    # Overall score should be substantially lower than senior
    senior_result = match(SENIOR_DEV_CANDIDATE, STANDARD_JOB)
    assert result.overall_score < senior_result.overall_score


def test_alias_candidate_skill_resolution():
    result = match(ALIAS_CANDIDATE, STANDARD_JOB)
    # Candidate skills: ["py", "js", "postgres", "reactjs", "node"]
    # Job required: ["Python", "PostgreSQL", "Docker"]
    # "py" -> Python, "postgres" -> PostgreSQL
    assert "Python" in result.matched_required_skills
    assert "PostgreSQL" in result.matched_required_skills
    assert "Docker" in result.missing_required_skills


def test_project_skill_candidate_skill_detection():
    # Diana has skills declared as empty list, but Python, Docker, PostgreSQL mentioned in project description
    result = match(PROJECT_SKILL_CANDIDATE, STANDARD_JOB)
    assert "Python" in result.matched_required_skills
    assert "PostgreSQL" in result.matched_required_skills
    assert "Docker" in result.matched_required_skills
    assert result.missing_required_skills == []


def test_self_taught_candidate_education_gap():
    result = match(SELF_TAUGHT_CANDIDATE, STANDARD_JOB)
    # Skills and experience satisfied, but education missing
    assert result.skill_score == 80.0  # All required skills matched (80% of total skill weight)
    assert result.experience_score == 100.0  # 4 years >= 3
    assert result.education_score == 0.0
    assert result.education_result == "Candidate education not specified or detected"
    # Still good match due to skills and experience
    assert result.overall_score >= 60.0


def test_empty_candidate_zero_scores():
    result = match(EMPTY_CANDIDATE, STANDARD_JOB)
    assert result.overall_score == 0.0
    assert result.skill_score == 0.0
    assert result.experience_score == 0.0
    assert result.education_score == 0.0
    assert result.text_similarity_score == 0.0
    assert len(result.missing_required_skills) == 3


def test_no_requirements_job():
    result = match(SENIOR_DEV_CANDIDATE, NO_REQUIREMENTS_JOB)
    assert result.education_result == "No education requirement specified"
    assert result.experience_result == "No experience requirement specified"
    assert result.education_score == 100.0
    assert result.experience_score == 100.0
