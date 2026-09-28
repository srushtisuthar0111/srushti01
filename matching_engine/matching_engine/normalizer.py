"""Normalization utilities for text and skill strings."""

from __future__ import annotations

import re
from typing import Any, Iterable

from matching_engine.config import MAX_TEXT_LENGTH, SKILL_ALIASES


def normalize_skill(skill: Any) -> str:
    """Normalize a single skill string: lowercase, strip, collapse spaces, alias resolution."""
    if skill is None:
        return ""
    text = str(skill).lower().strip()
    # Collapse multiple whitespace characters into a single space
    text = re.sub(r"\s+", " ", text)
    if not text:
        return ""
    # Resolve aliases (e.g. js -> javascript, py -> python)
    return SKILL_ALIASES.get(text, text)


def normalize_skills(skills: Iterable[Any]) -> list[str]:
    """Normalize and deduplicate an iterable of skills while preserving order."""
    seen = set()
    result = []
    for item in skills:
        norm = normalize_skill(item)
        if norm and norm not in seen:
            seen.add(norm)
            result.append(norm)
    return result


def clean_text(text: Any, max_length: int = MAX_TEXT_LENGTH) -> str:
    """Safely convert input to string and enforce maximum length."""
    if text is None:
        return ""
    text_str = str(text).strip()
    if len(text_str) > max_length:
        return text_str[:max_length]
    return text_str
