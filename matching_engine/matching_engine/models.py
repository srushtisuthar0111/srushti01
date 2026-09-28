"""Data models for candidate profile, job profile, and match result."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


def _coerce_list(val: Any) -> list[Any]:
    """Coerce various input types to a list safely."""
    if val is None:
        return []
    if isinstance(val, list):
        return val
    if isinstance(val, (tuple, set)):
        return list(val)
    if isinstance(val, str):
        # Support comma-separated strings if passed
        parts = [p.strip() for p in val.split(",") if p.strip()]
        return parts if parts else ([val.strip()] if val.strip() else [])
    return [val]


def _coerce_str_list(val: Any) -> list[str]:
    """Coerce input to a list of strings."""
    raw = _coerce_list(val)
    result = []
    for item in raw:
        if item is not None:
            text = str(item).strip()
            if text:
                result.append(text)
    return result


@dataclass
class CandidateProfile:
    name: str = ""
    email: str = ""
    skills: list[str] = field(default_factory=list)
    education: list[Any] = field(default_factory=list)
    experience: list[Any] = field(default_factory=list)
    projects: list[Any] = field(default_factory=list)

    def __post_init__(self) -> None:
        self.name = str(self.name or "").strip()
        self.email = str(self.email or "").strip()
        self.skills = _coerce_str_list(self.skills)
        self.education = _coerce_list(self.education)
        self.experience = _coerce_list(self.experience)
        self.projects = _coerce_list(self.projects)

    @classmethod
    def from_dict(cls, data: Any) -> CandidateProfile:
        if isinstance(data, CandidateProfile):
            return data
        if not isinstance(data, dict):
            return cls()
        return cls(
            name=data.get("name", ""),
            email=data.get("email", ""),
            skills=data.get("skills", []),
            education=data.get("education", []),
            experience=data.get("experience", []),
            projects=data.get("projects", []),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "email": self.email,
            "skills": list(self.skills),
            "education": list(self.education),
            "experience": list(self.experience),
            "projects": list(self.projects),
        }


@dataclass
class JobProfile:
    title: str = ""
    required_skills: list[str] = field(default_factory=list)
    preferred_skills: list[str] = field(default_factory=list)
    education: list[Any] = field(default_factory=list)
    experience: list[Any] = field(default_factory=list)
    description: str = ""

    def __post_init__(self) -> None:
        self.title = str(self.title or "").strip()
        self.required_skills = _coerce_str_list(self.required_skills)
        self.preferred_skills = _coerce_str_list(self.preferred_skills)
        self.education = _coerce_list(self.education)
        self.experience = _coerce_list(self.experience)
        self.description = str(self.description or "").strip()

    @classmethod
    def from_dict(cls, data: Any) -> JobProfile:
        if isinstance(data, JobProfile):
            return data
        if not isinstance(data, dict):
            return cls()
        return cls(
            title=data.get("title", ""),
            required_skills=data.get("required_skills", []),
            preferred_skills=data.get("preferred_skills", []),
            education=data.get("education", []),
            experience=data.get("experience", []),
            description=data.get("description", ""),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "title": self.title,
            "required_skills": list(self.required_skills),
            "preferred_skills": list(self.preferred_skills),
            "education": list(self.education),
            "experience": list(self.experience),
            "description": self.description,
        }


@dataclass
class MatchResult:
    overall_score: float
    skill_score: float
    experience_score: float
    education_score: float
    text_similarity_score: float
    matched_required_skills: list[str]
    missing_required_skills: list[str]
    matched_preferred_skills: list[str]
    education_result: str
    experience_result: str
    recommendation: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "overall_score": round(float(self.overall_score), 2),
            "skill_score": round(float(self.skill_score), 2),
            "experience_score": round(float(self.experience_score), 2),
            "education_score": round(float(self.education_score), 2),
            "text_similarity_score": round(float(self.text_similarity_score), 2),
            "matched_required_skills": list(self.matched_required_skills),
            "missing_required_skills": list(self.missing_required_skills),
            "matched_preferred_skills": list(self.matched_preferred_skills),
            "education_result": str(self.education_result),
            "experience_result": str(self.experience_result),
            "recommendation": str(self.recommendation),
        }

    def explain(self) -> str:
        """Return a formatted human-readable match explanation."""
        from matching_engine.explain import explain
        return explain(self)
