# Pure Python AI Resume–Job Matching Engine

An independent, zero-dependency matching engine built for the AI Resume–Job Matching Platform.

> **Mandatory Disclaimer**:  
> *"This platform provides decision-support recommendations based on job-related profile information. Recruiters remain responsible for all final hiring decisions."*

---

## 1. Project Overview

This package implements the core matching engine responsible for calculating compatibility between a candidate's profile and a job opening.

- **Zero External Dependencies**: Operates strictly using the Python standard library (`math`, `re`, `collections`, `dataclasses`).
- **Parallel Independence**: Completely decoupled from database schemas, Flask web frameworks, authentication, and file parsers.
- **Contract-Compliant**: Strict adherence to the shared `CandidateProfile`, `JobProfile`, and `MatchResult` data contracts.
- **Deterministic & Explainable**: Computes transparent subscores, produces clear rationales, and assigns structured recommendation tiers.

---

## 2. Architecture & Pipeline

```
CandidateProfile + JobProfile
             │
             ├──► 1. Skills Matching (50%)
             │       - Required vs. Preferred distinction
             │       - Alias resolution (e.g. py -> python, reactjs -> react)
             │       - Contextual match in project & experience text
             │
             ├──► 2. Experience Scoring (20%)
             │       - Transparent ratio bands (100%, 75%, 50%, 25%)
             │       - Tolerant parsing (years, months, date ranges)
             │
             ├──► 3. Education Scoring (15%)
             │       - Canonical hierarchy (High School -> Diploma -> Bachelor -> Master -> PhD)
             │       - Flexible degree alias matching (B.Tech, B.Sc, M.Tech, MBA, etc.)
             │
             └──► 4. Text Similarity (15%)
                     - Standard-library TF-IDF vectorization
                     - Cosine similarity calculation
                     │
                     ▼
         Weighted Aggregation & Clamping (0.0 - 100.0)
                     │
                     ▼
         Structured Explanation & Recommendation Tier
                     │
                     ▼
                MatchResult
```

---

## 3. Directory & File Structure

```
matching_engine/
├── pyproject.toml                     # PEP 621 package metadata
├── requirements-dev.txt               # Developer dependencies (pytest)
├── README.md                          # Documentation and integration guide
├── example.py                         # Standalone runner demonstrating usage
├── matching_engine/
│   ├── __init__.py                    # Public API exports
│   ├── __main__.py                    # CLI executable entrypoint (`python -m matching_engine`)
│   ├── config.py                      # Weights, education tiers, aliases, disclaimer
│   ├── education.py                   # Degree hierarchy & education scoring
│   ├── engine.py                      # Pipeline coordinator & main `match()` entrypoint
│   ├── experience.py                  # Experience parsing, date ranges, and scoring
│   ├── explain.py                     # Human-readable report generator
│   ├── models.py                      # Data models: CandidateProfile, JobProfile, MatchResult
│   ├── normalizer.py                  # Text and skill normalization utilities
│   ├── scoring.py                     # Weighted aggregation & 0-100 clamping
│   ├── skills.py                      # Required/preferred skill evaluation & alias resolver
│   └── text_similarity.py             # Pure Python TF-IDF and cosine similarity
└── tests/
    ├── __init__.py
    ├── fixtures.py                    # Contract-compliant mock candidate & job fixtures
    ├── test_contract.py               # Shared data contract & disclaimer validation
    ├── test_edge_cases.py             # Extreme inputs, malformed types, security payloads
    ├── test_education.py              # Degree tiers, aliases, satisfaction bands
    ├── test_engine.py                 # End-to-end integration scenarios
    ├── test_experience.py             # Experience parsing, date ranges, and band evaluation
    ├── test_scoring.py                # Weights validation, precision, and normalization
    ├── test_skills.py                 # Skill normalization, aliases, preferred penalties
    └── test_text_similarity.py        # Tokenization, TF-IDF, and cosine similarity
```

---

## 4. Dependencies

- **Production**: Python `>= 3.10` with standard library only. No external packages required.
- **Development & Testing**: `pytest >= 7.0.0`

---

## 5. Installation Commands

To install in editable mode for local development:

```powershell
# Navigate to the matching_engine directory
cd matching_engine

# Install dev dependencies
pip install -r requirements-dev.txt

# Install matching_engine package in editable mode
pip install -e .
```

---

## 6. Run Commands

### Run the Interactive CLI Demo

```powershell
# Formatted human-readable report
python -m matching_engine

# Raw contract-compliant JSON output
python -m matching_engine --json
```

### Run the Standalone Example Script

```powershell
python example.py
```

---

## 7. Test Commands

Run the full automated test suite:

```powershell
# From the matching_engine directory
python -m pytest -v
```

---

## 8. Integration Contract

### Input Contracts

#### `CandidateProfile`
```python
{
    "name": "Jane Doe",
    "email": "jane@example.com",
    "skills": ["Python", "Docker", "PostgreSQL"],
    "education": ["B.Tech in Computer Science"],
    "experience": ["4 years as Software Engineer"],
    "projects": [
        {
            "name": "Distributed Pipeline",
            "description": "Built event-driven ETL services with Python and Kafka."
        }
    ]
}
```

#### `JobProfile`
```python
{
    "title": "Senior Backend Developer",
    "required_skills": ["Python", "PostgreSQL", "Docker"],
    "preferred_skills": ["AWS", "Kubernetes"],
    "education": ["Bachelor degree in Computer Science or related"],
    "experience": ["3+ years"],
    "description": "Looking for a backend engineer experienced in Python, PostgreSQL, and cloud deployments."
}
```

### Output Contract (`MatchResult`)

```python
{
    "overall_score": 85.98,
    "skill_score": 90.0,
    "experience_score": 100.0,
    "education_score": 100.0,
    "text_similarity_score": 39.86,
    "matched_required_skills": ["Python", "PostgreSQL", "Docker"],
    "missing_required_skills": [],
    "matched_preferred_skills": ["AWS"],
    "education_result": "Requirement satisfied",
    "experience_result": "Requirement satisfied",
    "recommendation": "Strong match: Profile demonstrates high alignment with job criteria."
}
```

---

## 9. Integration Instructions for Team Members

### For Developer 1 (Job Management & Flask Platform)

When matching jobs against candidates in Flask route handlers or background tasks:

```python
from matching_engine import JobProfile, match

# In your route / service:
job = JobProfile.from_dict({
    "title": db_job.title,
    "required_skills": db_job.required_skills,   # List of strings or comma-separated string
    "preferred_skills": db_job.preferred_skills,
    "education": [db_job.education_level],
    "experience": [f"{db_job.min_experience_years} years"],
    "description": db_job.description,
})

# Execute match:
result = match(candidate_profile_dict, job)

# Save or render results:
result_dict = result.to_dict()
overall_score = result.overall_score
report_text = result.explain()
```

### For Developer 2 (Resume Extraction & Candidate Profile)

When parsing resumes and generating candidate profiles:

```python
from matching_engine import CandidateProfile, match

# In your resume extraction pipeline:
candidate = CandidateProfile.from_dict({
    "name": parsed_data["name"],
    "email": parsed_data["email"],
    "skills": parsed_data["skills"],             # list of strings
    "education": parsed_data["education_list"],  # list of strings or dicts
    "experience": parsed_data["experience_list"],# list of strings or dicts
    "projects": parsed_data["projects_list"],
})

# Pass directly to the engine:
result = match(candidate, job_profile_dict)
```

---

## 10. Security Assurance

The matching engine processes all profile text as inert string data. It contains no database drivers, executes no SQL commands, runs no `eval`/`exec`, and invokes no subshells.
