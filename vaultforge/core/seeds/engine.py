"""Seed engine: creates a clean, deduplicated initial corpus."""
from __future__ import annotations

from collections.abc import Mapping

from vaultforge.core.utils.text import (
    NormalizedSeed,
    classify_seed,
    normalize_optional,
    normalize_unicode,
    transliterate,
)

SEED_PRIORITIES: dict[str, float] = {
    "name": 1.00,
    "surname": 0.92,
    "nickname": 0.90,
    "pet": 0.82,
    "relationship": 0.78,
    "year": 0.76,
    "game": 0.64,
    "team": 0.62,
    "band": 0.58,
    "anime": 0.57,
    "movie": 0.52,
    "city": 0.45,
    "phrase": 0.42,
}


def build_seeds(inputs: Mapping[str, str | None]) -> list[NormalizedSeed]:
    """Build normalized seeds from optional user fields.

    Empty strings and explicit skip values (``none``, ``null``, ``skip``) are ignored.
    Unicode-preserving and ASCII-transliterated variants are retained by the seed object.
    """
    seen: set[str] = set()
    seeds: list[NormalizedSeed] = []
    for category, raw in inputs.items():
        optional = normalize_optional(raw)
        if not optional:
            continue
        normalized = normalize_unicode(optional)
        ascii_value = transliterate(normalized) or None
        key = f"{category}:{normalized}:{ascii_value}"
        if key in seen:
            continue
        seen.add(key)
        seeds.append(
            NormalizedSeed(
                original=optional,
                normalized=normalized,
                transliterated=ascii_value,
                category=category,
                priority=SEED_PRIORITIES.get(category, 0.50),
                classification=classify_seed(normalized),
            )
        )
    return seeds
