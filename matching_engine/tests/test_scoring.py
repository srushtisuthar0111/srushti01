"""Tests for weighted score calculation, 0-100 normalization, and recommendation tiers."""

from matching_engine.config import RECOMMENDATION_TIERS, WEIGHTS
from matching_engine.explain import get_recommendation
from matching_engine.scoring import calculate_overall_score


def test_weights_sum_to_one():
    total_weights = sum(WEIGHTS.values())
    assert abs(total_weights - 1.0) < 1e-6
    assert WEIGHTS["skills"] == 0.50
    assert WEIGHTS["experience"] == 0.20
    assert WEIGHTS["education"] == 0.15
    assert WEIGHTS["text"] == 0.15


def test_perfect_score():
    score = calculate_overall_score(100.0, 100.0, 100.0, 100.0)
    assert score == 100.0


def test_zero_score():
    score = calculate_overall_score(0.0, 0.0, 0.0, 0.0)
    assert score == 0.0


def test_weighted_calculation():
    # 50% * 80 + 20% * 60 + 15% * 100 + 15% * 40
    # = 40 + 12 + 15 + 6 = 73.0
    score = calculate_overall_score(80.0, 60.0, 100.0, 40.0)
    assert score == 73.0


def test_clamping_upper_and_lower_bounds():
    # Edge case where upstream might give out-of-bounds numbers
    score_over = calculate_overall_score(150.0, 120.0, 110.0, 105.0)
    assert score_over == 100.0

    score_under = calculate_overall_score(-20.0, -10.0, -50.0, 0.0)
    assert score_under == 0.0


def test_rounding_precision():
    # 50% * 33.33 + 20% * 66.66 + 15% * 77.77 + 15% * 88.88
    # 16.665 + 13.332 + 11.6655 + 13.332 = 54.9945 -> 54.99
    score = calculate_overall_score(33.33, 66.66, 77.77, 88.88)
    assert isinstance(score, float)
    assert score == round(score, 2)


def test_recommendation_tiers():
    assert "Strong match" in get_recommendation(95.0)
    assert "Strong match" in get_recommendation(80.0)
    assert "Good match" in get_recommendation(79.9)
    assert "Good match" in get_recommendation(60.0)
    assert "Partial match" in get_recommendation(59.9)
    assert "Partial match" in get_recommendation(40.0)
    assert "Low match" in get_recommendation(39.9)
    assert "Low match" in get_recommendation(0.0)
