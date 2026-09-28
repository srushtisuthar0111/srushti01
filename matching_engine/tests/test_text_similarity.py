"""Tests for TF-IDF tokenization and cosine similarity calculations."""

import math
from matching_engine.config import MAX_TEXT_LENGTH
from matching_engine.text_similarity import (
    compute_text_similarity,
    compute_tfidf_vectors,
    cosine_similarity,
    tokenize,
)


def test_tokenize_filters_stopwords_and_short_tokens():
    text = "The quick brown fox and a lazy dog are jumping"
    tokens = tokenize(text)
    # "the", "and", "a", "are" are in STOPWORDS
    assert "the" not in tokens
    assert "and" not in tokens
    assert "a" not in tokens
    assert "are" not in tokens
    assert "quick" in tokens
    assert "brown" in tokens
    assert "fox" in tokens
    assert "lazy" in tokens
    assert "dog" in tokens
    assert "jumping" in tokens


def test_tokenize_empty_and_none():
    assert tokenize("") == []
    assert tokenize(None) == []
    assert tokenize("   ") == []


def test_tfidf_vectors_empty():
    vec1, vec2 = compute_tfidf_vectors([], [])
    assert vec1 == {}
    assert vec2 == {}


def test_cosine_similarity_empty():
    assert cosine_similarity({}, {}) == 0.0
    assert cosine_similarity({"python": 1.0}, {}) == 0.0
    assert cosine_similarity({}, {"python": 1.0}) == 0.0


def test_cosine_similarity_identical_vectors():
    vec = {"python": 0.5, "fastapi": 0.8, "docker": 0.3}
    assert math.isclose(cosine_similarity(vec, vec), 1.0, rel_tol=1e-5)


def test_cosine_similarity_orthogonal_vectors():
    vec1 = {"python": 1.0}
    vec2 = {"java": 1.0}
    assert cosine_similarity(vec1, vec2) == 0.0


def test_text_similarity_identical_text():
    text = "Senior Python engineer building microservices with FastAPI and PostgreSQL on AWS cloud infrastructure"
    score = compute_text_similarity(text, text)
    assert score >= 99.9  # Effectively 100.0


def test_text_similarity_completely_unrelated_text():
    text_cand = "Classical ballet dancer skilled in choreography, performance, and stage presence"
    text_job = "DevOps infrastructure engineer experienced in Kubernetes, Terraform, and Linux administration"
    score = compute_text_similarity(text_cand, text_job)
    assert score == 0.0


def test_text_similarity_empty_inputs():
    assert compute_text_similarity("", "") == 0.0
    assert compute_text_similarity(None, "Software Engineer") == 0.0
    assert compute_text_similarity("Software Engineer", None) == 0.0
    assert compute_text_similarity(None, None) == 0.0


def test_text_similarity_short_text():
    cand = "Python developer"
    job = "Python developer"
    score = compute_text_similarity(cand, job)
    assert score > 90.0


def test_text_similarity_partial_overlap():
    cand = "Python backend developer with PostgreSQL experience and AWS deployment knowledge"
    job = "Looking for a Python developer who knows Docker and Kubernetes for cloud apps"
    score = compute_text_similarity(cand, job)
    assert 0.0 < score < 100.0


def test_text_similarity_exceeding_max_length():
    # Long text exceeding MAX_TEXT_LENGTH
    cand_long = ("Python microservices and distributed database architecture " * 2000)[:MAX_TEXT_LENGTH + 1000]
    job_long = ("Python cloud systems development with PostgreSQL and Docker " * 2000)[:MAX_TEXT_LENGTH + 1000]
    # Must process without crashing or memory exhaustion
    score = compute_text_similarity(cand_long, job_long)
    assert 0.0 <= score <= 100.0
