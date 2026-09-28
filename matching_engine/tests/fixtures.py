"""Local test fixtures and mock data. No external dependencies."""

SENIOR_DEV_CANDIDATE = {
    "name": "Alice Senior",
    "email": "alice@example.com",
    "skills": ["Python", "PostgreSQL", "Docker", "AWS", "FastAPI"],
    "education": ["B.Tech in Computer Science and Engineering"],
    "experience": ["5 years as Senior Software Engineer at Tech Corp"],
    "projects": [
        {
            "name": "Cloud Microservices",
            "description": "Architected distributed systems deployed on AWS with Kubernetes.",
        }
    ],
}

JUNIOR_DEV_CANDIDATE = {
    "name": "Bob Junior",
    "email": "bob@example.com",
    "skills": ["Python", "HTML", "CSS"],
    "education": ["High School Diploma"],
    "experience": ["1 year as Junior Developer at Startup"],
    "projects": [
        "Built responsive static websites using HTML and CSS."
    ],
}

ALIAS_CANDIDATE = {
    "name": "Charlie Alias",
    "email": "charlie@example.com",
    "skills": ["py", "js", "postgres", "reactjs", "node"],
    "education": ["Bachelor of Science"],
    "experience": ["3 years software development"],
    "projects": [],
}

PROJECT_SKILL_CANDIDATE = {
    "name": "Diana Project",
    "email": "diana@example.com",
    "skills": [],
    "education": ["B.E. Information Technology"],
    "experience": ["Jan 2021 - Mar 2023"],
    "projects": [
        {
            "title": "Data Pipeline",
            "description": "Implemented automated ETL using Python, Docker, and PostgreSQL database.",
        }
    ],
}

SELF_TAUGHT_CANDIDATE = {
    "name": "Evan SelfTaught",
    "email": "evan@example.com",
    "skills": ["Python", "PostgreSQL", "Docker"],
    "education": [],
    "experience": ["4 years professional software engineering"],
    "projects": [],
}

EMPTY_CANDIDATE = {
    "name": "",
    "email": "",
    "skills": [],
    "education": [],
    "experience": [],
    "projects": [],
}

STANDARD_JOB = {
    "title": "Senior Python Developer",
    "required_skills": ["Python", "PostgreSQL", "Docker"],
    "preferred_skills": ["AWS", "Kubernetes"],
    "education": ["Bachelor degree in Computer Science or related field"],
    "experience": ["3+ years"],
    "description": "Looking for a seasoned Python engineer experienced with PostgreSQL, Docker containerization, and AWS cloud services.",
}

ENTRY_JOB = {
    "title": "Junior Web Developer",
    "required_skills": ["JavaScript", "HTML", "CSS"],
    "preferred_skills": ["React"],
    "education": ["Diploma or Bachelor"],
    "experience": ["1-2 years"],
    "description": "Entry level web developer role writing clean HTML, CSS, and modern JavaScript.",
}

NO_REQUIREMENTS_JOB = {
    "title": "General Associate",
    "required_skills": [],
    "preferred_skills": [],
    "education": [],
    "experience": [],
    "description": "",
}
