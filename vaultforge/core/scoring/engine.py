"""Behavioral scoring for analyzed passwords."""
from __future__ import annotations

from dataclasses import dataclass

from vaultforge.core.entropy.engine import entropy_bits
from vaultforge.core.rules.patterns import match_patterns

PENALTIES = {
    "personal_seed": 28,
    "false_complexity": 26,
    "common_suffix": 18,
    "common_year": 16,
    "basic_leetspeak": 13,
    "predictable_capitalization": 10,
    "keyboard_walk": 22,
    "repetition": 16,
}


@dataclass(frozen=True)
class PasswordAnalysis:
    password: str
    entropy: float
    human_predictability: str
    perceived_strength: str
    real_resistance: str
    matched_patterns: tuple[str, ...]
    score_breakdown: dict[str, str]


def _band(value: float, high_bad: bool = False) -> str:
    if high_bad:
        if value >= 70:
            return "HIGH"
        if value >= 40:
            return "MEDIUM"
        return "LOW"
    if value >= 70:
        return "HIGH"
    if value >= 40:
        return "MEDIUM"
    return "LOW"


def analyze_password(password: str, personal_seeds: set[str] | None = None) -> PasswordAnalysis:
    entropy = entropy_bits(password)
    patterns = tuple(match_patterns(password, personal_seeds))
    predictability = min(100, sum(PENALTIES.get(pattern, 8) for pattern in patterns))
    perceived = _band(entropy)
    resistance_score = max(0, min(100, entropy - predictability))
    return PasswordAnalysis(
        password=password,
        entropy=entropy,
        human_predictability=_band(predictability, high_bad=True),
        perceived_strength=perceived,
        real_resistance=_band(resistance_score),
        matched_patterns=patterns,
        score_breakdown={
            "Human Predictability": _band(predictability, high_bad=True),
            "Entropy": perceived,
            "Mutation Resistance": _band(resistance_score),
            "Dictionary Resistance": "VERY LOW" if "personal_seed" in patterns or "false_complexity" in patterns else _band(resistance_score),
        },
    )
