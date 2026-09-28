"""Matching Engine package exports."""

from matching_engine.config import DISCLAIMER
from matching_engine.engine import match
from matching_engine.explain import explain
from matching_engine.models import CandidateProfile, JobProfile, MatchResult

__all__ = [
    "match",
    "CandidateProfile",
    "JobProfile",
    "MatchResult",
    "DISCLAIMER",
    "explain",
]
