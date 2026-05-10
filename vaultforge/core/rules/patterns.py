"""Common human password patterns."""
from __future__ import annotations

import re

KEYBOARD_WALKS = ("qwerty", "asdfgh", "qazwsx", "1q2w3e", "zaq12wsx")
FALSE_COMPLEXITY = ("p@ssw0rd", "admin123", "qwerty@", "password", "senha")
COMMON_YEARS_RE = re.compile(r"(?:19[9][0-9]|20[0-2][0-9])")
REPETITION_RE = re.compile(r"(.{1,3})\1{2,}", re.IGNORECASE)


def match_patterns(password: str, seeds: set[str] | None = None) -> list[str]:
    lowered = password.lower()
    matches: list[str] = []
    if seeds and any(seed and seed in lowered for seed in seeds):
        matches.append("personal_seed")
    if any(walk in lowered for walk in KEYBOARD_WALKS):
        matches.append("keyboard_walk")
    if any(pattern in lowered for pattern in FALSE_COMPLEXITY):
        matches.append("false_complexity")
    if COMMON_YEARS_RE.search(lowered):
        matches.append("common_year")
    if re.search(r"(?:123|1234|@123|!!?)$", lowered):
        matches.append("common_suffix")
    if REPETITION_RE.search(lowered):
        matches.append("repetition")
    if any(char in lowered for char in "@4310$7"):
        matches.append("basic_leetspeak")
    if password[:1].isupper() and password[1:].lower() == password[1:]:
        matches.append("predictable_capitalization")
    return matches
