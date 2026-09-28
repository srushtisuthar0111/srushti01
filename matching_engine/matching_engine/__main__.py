"""CLI runner and demo for the matching engine."""

from __future__ import annotations

import argparse
import json
import sys

from matching_engine.engine import match
from matching_engine.models import CandidateProfile, JobProfile


DEMO_CANDIDATE = {
    "name": "Alex Mercer",
    "email": "alex.mercer@example.com",
    "skills": ["Python", "PostgreSQL", "Docker", "AWS", "FastAPI"],
    "education": ["B.Tech in Computer Science"],
    "experience": ["4 years as Backend Engineer"],
    "projects": [
        {
            "name": "Cloud API Gateway",
            "description": "Designed asynchronous REST microservices using Python, FastAPI, and PostgreSQL on AWS.",
        }
    ],
}

DEMO_JOB = {
    "title": "Senior Backend Developer",
    "required_skills": ["Python", "PostgreSQL", "Docker"],
    "preferred_skills": ["AWS", "Kubernetes"],
    "education": ["Bachelor degree in Computer Science or related"],
    "experience": ["3+ years"],
    "description": "We are seeking a Backend Developer proficient in Python, PostgreSQL, and Docker containerization. Experience with AWS cloud infrastructure is a plus.",
}


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="python -m matching_engine",
        description="Pure Python AI Resume-Job Matching Engine Demo Runner",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output raw JSON according to MatchResult shared contract",
    )
    args = parser.parse_args()

    candidate = CandidateProfile.from_dict(DEMO_CANDIDATE)
    job = JobProfile.from_dict(DEMO_JOB)

    result = match(candidate, job)

    if args.json:
        print(json.dumps(result.to_dict(), indent=2))
    else:
        print(result.explain())

    return 0


if __name__ == "__main__":
    sys.exit(main())
