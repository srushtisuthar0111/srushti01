"""Pure Python TF-IDF and cosine similarity implementation (standard library only)."""

from __future__ import annotations

from collections import Counter
import math
import re
from typing import Sequence

from matching_engine.config import MAX_TEXT_LENGTH, STOPWORDS


def tokenize(text: str | None) -> list[str]:
    """
    Tokenize text into lowercase alphanumeric words, filtering out stopwords.
    Handles None, unicode, and long text gracefully.
    """
    if not text:
        return []
    # Truncate to MAX_TEXT_LENGTH to avoid resource exhaustion
    safe_text = str(text)[:MAX_TEXT_LENGTH].lower()
    raw_tokens = re.findall(r"[a-zA-Z0-9]+", safe_text)
    return [tok for tok in raw_tokens if tok not in STOPWORDS and len(tok) > 1]


def compute_tfidf_vectors(
    doc1_tokens: Sequence[str],
    doc2_tokens: Sequence[str],
) -> tuple[dict[str, float], dict[str, float]]:
    """
    Compute smoothed TF-IDF vectors for two documents.
    Smoothed IDF formula: ln((1 + N) / (1 + DF)) + 1
    """
    tf1 = Counter(doc1_tokens)
    tf2 = Counter(doc2_tokens)
    vocab = set(tf1.keys()) | set(tf2.keys())

    if not vocab:
        return {}, {}

    n_docs = 2
    len1 = len(doc1_tokens)
    len2 = len(doc2_tokens)

    vec1: dict[str, float] = {}
    vec2: dict[str, float] = {}

    for term in vocab:
        df = (1 if term in tf1 else 0) + (1 if term in tf2 else 0)
        # Smoothed IDF ensures no division by zero and smooth scaling
        idf = math.log((1 + n_docs) / (1 + df)) + 1.0

        if len1 > 0 and term in tf1:
            vec1[term] = (tf1[term] / len1) * idf
        if len2 > 0 and term in tf2:
            vec2[term] = (tf2[term] / len2) * idf

    return vec1, vec2


def cosine_similarity(vec1: dict[str, float], vec2: dict[str, float]) -> float:
    """Compute cosine similarity between two term-weight vectors."""
    if not vec1 or not vec2:
        return 0.0

    common_terms = set(vec1.keys()) & set(vec2.keys())
    if not common_terms:
        return 0.0

    dot_product = sum(vec1[t] * vec2[t] for t in common_terms)
    norm1 = math.sqrt(sum(v * v for v in vec1.values()))
    norm2 = math.sqrt(sum(v * v for v in vec2.values()))

    if norm1 == 0.0 or norm2 == 0.0:
        return 0.0

    sim = dot_product / (norm1 * norm2)
    return max(0.0, min(1.0, sim))


def compute_text_similarity(candidate_text: str | None, job_text: str | None) -> float:
    """
    Compute text similarity score (0.0 - 100.0) between candidate and job text.
    Returns 0.0 for empty or unparseable inputs.
    """
    cand_tokens = tokenize(candidate_text)
    job_tokens = tokenize(job_text)

    if not cand_tokens or not job_tokens:
        return 0.0

    vec1, vec2 = compute_tfidf_vectors(cand_tokens, job_tokens)
    similarity = cosine_similarity(vec1, vec2)
    return round(similarity * 100.0, 2)
