"""Configuration defaults and safety limits."""
from __future__ import annotations

from dataclasses import dataclass

MAX_PASSWORDS_HARD_LIMIT = 1_000_000
DEFAULT_LIMIT = 100_000


@dataclass(frozen=True)
class GenerationConfig:
    max_passwords: int = DEFAULT_LIMIT
    enable_leetspeak: bool = True
    enable_keyboard_walks: bool = True
    aggressive_mode: bool = False
    threads: int = 1


def clamp_limit(limit: int | None) -> int:
    if limit is None:
        return DEFAULT_LIMIT
    return max(1, min(limit, MAX_PASSWORDS_HARD_LIMIT))
