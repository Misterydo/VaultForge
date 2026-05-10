"""Ranking engine for human-likelihood ordering."""
from __future__ import annotations

from collections.abc import Iterable

from vaultforge.core.mutations.engine import Candidate


def rank_candidates(candidates: Iterable[Candidate]) -> list[Candidate]:
    """Sort candidates by descending behavioral probability and stable password order."""
    return sorted(candidates, key=lambda item: (-item.score, len(item.password), item.password))
