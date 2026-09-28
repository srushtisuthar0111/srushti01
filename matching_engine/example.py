"""
Matching Engine Quickstart Example.
Demonstrates running matches with mock Candidate and Job profiles.
"""

from __future__ import annotations

import json
from matching_engine import CandidateProfile, JobProfile, match


def main() -> None:
    print("=" * 65)
    print(" AI Resume-Job Matching Engine - Quickstart Demonstration")
    print("=" * 65)

    # 1. Define Candidate Profile (can be raw dict or CandidateProfile dataclass)
    candidate_data = {
        "name": "Sarah Connor",
        "email": "sarah.connor@example.com",
        "skills": ["Python", "FastAPI", "PostgreSQL", "Docker", "AWS"],
        "education": ["B.Tech in Computer Science"],
        "experience": [
            {"title": "Software Engineer", "years": 3.5, "company": "Cyberdyne"}
        ],
        "projects": [
            {
                "name": "Resilient Microservices",
                "description": "Architected cloud services using Python, Docker, and AWS ECS.",
            }
        ],
    }

    # 2. Define Job Profile (can be raw dict or JobProfile dataclass)
    job_data = {
        "title": "Senior Cloud Backend Engineer",
        "required_skills": ["Python", "PostgreSQL", "Docker"],
        "preferred_skills": ["AWS", "Kubernetes"],
        "education": ["Bachelor degree in STEM"],
        "experience": ["3+ years"],
        "description": "Seeking an experienced backend engineer proficient in Python and PostgreSQL with Docker and AWS.",
    }

    print("\nMatching Candidate against Job...")
    result = match(candidate_data, job_data)

    print("\n--- 1. Match Result Summary ---")
    print(f"Overall Score:        {result.overall_score}/100")
    print(f"Skill Score:          {result.skill_score}/100")
    print(f"Experience Score:     {result.experience_score}/100 ({result.experience_result})")
    print(f"Education Score:      {result.education_score}/100 ({result.education_result})")
    print(f"Text Similarity:      {result.text_similarity_score}/100")
    print(f"Matched Req Skills:   {result.matched_required_skills}")
    print(f"Missing Req Skills:   {result.missing_required_skills}")
    print(f"Matched Pref Skills:  {result.matched_preferred_skills}")
    print(f"Recommendation:       {result.recommendation}")

    print("\n--- 2. Full Formatted Explanation Report ---")
    print(result.explain())

    print("\n--- 3. Contract-Compliant Dictionary ---")
    print(json.dumps(result.to_dict(), indent=2))


if __name__ == "__main__":
    main()
