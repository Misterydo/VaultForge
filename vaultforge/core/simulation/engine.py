"""Defensive local simulation against generated candidates."""
from __future__ import annotations

from dataclasses import dataclass

from vaultforge.core.mutations.engine import Candidate


@dataclass(frozen=True)
class SimulationResult:
    matched: bool
    attempts: int
    rule_matched: tuple[str, ...]
    estimated_resistance: str


def simulate_match(password: str, candidates: list[Candidate] | tuple[Candidate, ...]) -> SimulationResult:
    """Attempt to match a password against an in-memory defensive candidate stream."""
    for index, candidate in enumerate(candidates, start=1):
        if candidate.password == password:
            resistance = "LOW" if index < 100_000 else "MEDIUM"
            return SimulationResult(True, index, candidate.rules, resistance)
    return SimulationResult(False, len(candidates), (), "UNKNOWN")
