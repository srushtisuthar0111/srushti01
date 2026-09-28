You are Developer 3 of a 3-developer team building the AI Resume–Job Matching Platform described in the master project specification.

IMPORTANT PARALLEL-DEVELOPMENT RULE:

You are working simultaneously with Developer 1 and Developer 2 on completely different PCs.

DO NOT WAIT for their code.
DO NOT require their code to run your code.
DO NOT import their unfinished modules.
DO NOT ask them to create anything before you can continue.
DO NOT stop because another developer's module does not exist.

Your matching engine MUST run independently on a fresh machine.

==================================================
1. YOUR RESPONSIBILITY
==================================================

You own ONLY:

- Matching engine
- Skill matching
- Experience scoring
- Education scoring
- TF-IDF
- Cosine similarity
- Weighted scoring
- 0–100 normalization
- Match explanations
- Recommendations
- Match-result generation
- Matching unit tests
- Matching edge-case tests

You do NOT own:

- Database
- Authentication
- User management
- Resume PDF/DOCX extraction
- Flask application foundation

==================================================
2. MOST IMPORTANT ARCHITECTURE RULE
==================================================

The matching engine MUST be a pure Python module.

It must NOT depend on:

- Flask
- SQLAlchemy
- Database
- Login system
- HTML templates
- HTTP requests
- Uploaded files
- Developer 1's code
- Developer 2's code

Input:

CandidateProfile + JobProfile

Output:

MatchResult

Therefore you can build and test the entire matching engine without anyone else's code.

==================================================
3. SHARED DATA CONTRACT
==================================================

CandidateProfile:

{
    "name": "...",
    "email": "...",
    "skills": [],
    "education": [],
    "experience": [],
    "projects": []
}

JobProfile:

{
    "title": "...",
    "required_skills": [],
    "preferred_skills": [],
    "education": [],
    "experience": [],
    "description": "..."
}

MatchResult:

{
    "overall_score": 0.0,
    "skill_score": 0.0,
    "experience_score": 0.0,
    "education_score": 0.0,
    "text_similarity_score": 0.0,
    "matched_required_skills": [],
    "missing_required_skills": [],
    "matched_preferred_skills": [],
    "education_result": "",
    "experience_result": "",
    "recommendation": ""
}

These are fixed integration contracts.

==================================================
4. MATCHING WEIGHTS
==================================================

Use:

Skills = 0.50

Experience = 0.20

Education = 0.15

Text Similarity = 0.15

Store weights in configuration.

Do not hard-code them throughout the algorithm.

==================================================
5. MATCHING PIPELINE
==================================================

CandidateProfile
+
JobProfile

↓

Skill score

↓

Experience score

↓

Education score

↓

TF-IDF cosine similarity

↓

Weighted total

↓

Normalize to 0–100

↓

Explanation

↓

MatchResult

==================================================
6. SKILLS
==================================================

Required and preferred skills must be treated differently.

A missing preferred skill must NOT be penalized like a missing required skill.

Return:

- matched required skills
- missing required skills
- matched preferred skills

Test:

- exact matches
- case differences
- aliases
- missing skills
- empty skills
- all skills matched
- no skills matched

==================================================
7. EXPERIENCE
==================================================

Implement a transparent compatibility calculation.

Return an understandable result such as:

"Requirement satisfied"

or

"Close to requirement"

or another clearly documented result.

Do not use unexplained black-box scoring.

==================================================
8. EDUCATION
==================================================

Compare candidate education with job education requirements.

Return:

- education score
- education result

The logic must be deterministic and testable.

==================================================
9. TEXT SIMILARITY
==================================================

Use:

TF-IDF
+
cosine similarity

Compare relevant candidate/resume text with relevant job description text.

Handle:

- empty text
- identical text
- unrelated text
- short text
- normal text

without crashing.

==================================================
10. EXPLANATION
==================================================

Every result must explain why the score was produced.

Example structure:

Overall score
Skill result
Experience result
Education result
Text similarity result
Matched skills
Missing skills
Recommendation

Never present the result as an automatic hiring decision.

Use the required disclaimer:

"This platform provides decision-support recommendations based on job-related profile information. Recruiters remain responsible for all final hiring decisions."

==================================================
11. ZERO-DEPENDENCY TESTING
==================================================

Create your own mock data.

For example:

candidate_1 = CandidateProfile(...)

job_1 = JobProfile(...)

Then run:

match(candidate_1, job_1)

Do NOT import CandidateProfile from Developer 2.

Do NOT import JobProfile from Developer 1.

Define local contract-compatible test fixtures.

Later, the real application can pass the same structure into your engine.

==================================================
12. TESTING
==================================================

Create unit tests for:

- Skills
- Required skills
- Preferred skills
- Experience
- Education
- TF-IDF
- Cosine similarity
- Weight calculations
- Overall score
- 0–100 normalization
- Empty input
- Missing fields
- Extreme cases
- Result format

The entire matching package must pass tests without Flask, PostgreSQL, or another developer's code.

==================================================
13. SECURITY
==================================================

The matching engine must not execute:

- SQL
- arbitrary code
- shell commands
- uploaded content as code

Treat all input as data.

