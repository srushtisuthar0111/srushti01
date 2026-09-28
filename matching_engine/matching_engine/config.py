"""Configuration constants for the matching engine."""

# Weights for overall score computation - must strictly sum to 1.0
WEIGHTS: dict[str, float] = {
    "skills": 0.50,
    "experience": 0.20,
    "education": 0.15,
    "text": 0.15,
}

assert abs(sum(WEIGHTS.values()) - 1.0) < 1e-6, "WEIGHTS must sum to 1.0"

# Default score when neither required nor preferred skills are specified
DEFAULT_NEUTRAL_SKILL_SCORE: float = 50.0

# Education level hierarchy (higher number = higher qualification)
EDUCATION_LEVELS: dict[str, int] = {
    "high school": 1,
    "diploma": 2,
    "bachelor": 3,
    "master": 4,
    "phd": 5,
}

# Aliases and variations mapped to canonical education level
EDUCATION_ALIASES: dict[str, str] = {
    # High School
    "high school diploma": "high school",
    "high school": "high school",
    "secondary school": "high school",
    "secondary": "high school",
    "higher secondary": "high school",
    "10th": "high school",
    "12th": "high school",
    "ged": "high school",
    "hsc": "high school",
    "ssc": "high school",
    # Diploma
    "diploma": "diploma",
    "polytechnic": "diploma",
    "associate": "diploma",
    "associates": "diploma",
    # Bachelor
    "bachelor": "bachelor",
    "bachelors": "bachelor",
    "btech": "bachelor",
    "b.tech": "bachelor",
    "be": "bachelor",
    "b.e": "bachelor",
    "b.e.": "bachelor",
    "bsc": "bachelor",
    "b.sc": "bachelor",
    "b.sc.": "bachelor",
    "bs": "bachelor",
    "b.s": "bachelor",
    "b.s.": "bachelor",
    "bca": "bachelor",
    "bba": "bachelor",
    "undergraduate": "bachelor",
    # Master
    "master": "master",
    "masters": "master",
    "mtech": "master",
    "m.tech": "master",
    "me": "master",
    "m.e": "master",
    "m.e.": "master",
    "msc": "master",
    "m.sc": "master",
    "m.sc.": "master",
    "ms": "master",
    "m.s": "master",
    "m.s.": "master",
    "mca": "master",
    "mba": "master",
    "postgraduate": "master",
    # PhD
    "phd": "phd",
    "ph.d": "phd",
    "ph.d.": "phd",
    "doctorate": "phd",
    "doctoral": "phd",
}

# Skill synonyms and aliases normalized to a canonical term
SKILL_ALIASES: dict[str, str] = {
    "js": "javascript",
    "py": "python",
    "ml": "machine learning",
    "ai": "artificial intelligence",
    "dl": "deep learning",
    "nlp": "natural language processing",
    "postgres": "postgresql",
    "postgresql": "postgresql",
    "reactjs": "react",
    "react.js": "react",
    "node": "node.js",
    "nodejs": "node.js",
    "node.js": "node.js",
    "ts": "typescript",
    "golang": "go",
    "k8s": "kubernetes",
    "aws": "amazon web services",
    "gcp": "google cloud platform",
    "azure": "microsoft azure",
    "tf": "tensorflow",
    "sklearn": "scikit-learn",
    "mongo": "mongodb",
    "cpp": "c++",
    "csharp": "c#",
}

# Recommendation tiers based on overall score (threshold, recommendation label)
RECOMMENDATION_TIERS: list[tuple[float, str]] = [
    (80.0, "Strong match: Profile demonstrates high alignment with job criteria."),
    (60.0, "Good match: Candidate meets most core requirements."),
    (40.0, "Partial match: Candidate meets some requirements; review gaps."),
    (0.0, "Low match: Significant gaps in required skills or experience."),
]

# Maximum text length to process for TF-IDF to prevent performance degradation
MAX_TEXT_LENGTH: int = 50_000

# Stopwords for text tokenization (standard English stopwords)
STOPWORDS: set[str] = {
    "a", "about", "above", "after", "again", "against", "all", "am", "an", "and",
    "any", "are", "aren't", "as", "at", "be", "because", "been", "before", "being",
    "below", "between", "both", "but", "by", "can", "cannot", "could", "did", "do",
    "does", "doing", "don't", "down", "during", "each", "few", "for", "from", "further",
    "had", "has", "have", "having", "he", "her", "here", "hers", "herself", "him",
    "himself", "his", "how", "i", "if", "in", "into", "is", "isn't", "it", "its",
    "itself", "let's", "me", "more", "most", "mustn't", "my", "myself", "no", "nor",
    "not", "of", "off", "on", "once", "only", "or", "other", "ought", "our", "ours",
    "ourselves", "out", "over", "own", "same", "she", "should", "so", "some", "such",
    "than", "that", "the", "their", "theirs", "them", "themselves", "then", "there",
    "these", "they", "this", "those", "through", "to", "too", "under", "until", "up",
    "very", "was", "wasn't", "we", "were", "weren't", "what", "when", "where", "which",
    "while", "who", "whom", "why", "with", "won't", "would", "you", "your", "yours",
    "yourself", "yourselves"
}

# Mandatory platform disclaimer
DISCLAIMER: str = (
    "This platform provides decision-support recommendations based on job-related profile information. "
    "Recruiters remain responsible for all final hiring decisions."
)
