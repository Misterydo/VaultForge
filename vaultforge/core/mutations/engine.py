"""Human-oriented mutation chains."""
from __future__ import annotations

from collections.abc import Iterable, Iterator
from dataclasses import dataclass

from vaultforge.core.utils.text import NormalizedSeed

LEET_PARTIAL = (("a", "@"), ("e", "3"), ("i", "1"), ("o", "0"), ("s", "$"), ("t", "7"))
COMMON_SUFFIXES = ("123", "1234", "!", "!!", "@123")
COMMON_PREFIXES = ("@", "#", "_", ".", "xX_")

MUTATION_WEIGHTS: dict[str, float] = {
    "identity": 1.00,
    "append_123": 0.98,
    "append_year": 0.91,
    "capitalize_first": 0.84,
    "append_symbol": 0.80,
    "replace_a_@": 0.77,
    "partial_leet": 0.74,
    "prefix_symbol": 0.40,
    "edgy_wrap": 0.18,
}


@dataclass(frozen=True)
class Candidate:
    password: str
    score: float
    seed_category: str
    rules: tuple[str, ...]


def _capitalize_first(value: str) -> str:
    return value[:1].upper() + value[1:] if value else value


def _partial_leet(value: str) -> Iterator[tuple[str, str]]:
    lower = value.lower()
    for src, dst in LEET_PARTIAL:
        index = lower.find(src)
        if index >= 0:
            yield value[:index] + dst + value[index + 1 :], f"replace_{src}_{dst}"


def _base_variants(seed: NormalizedSeed) -> Iterator[Candidate]:
    for variant in seed.variants():
        yield Candidate(variant, seed.priority, seed.category, ("identity",))
        cap = _capitalize_first(variant)
        if cap != variant:
            yield Candidate(cap, seed.priority * MUTATION_WEIGHTS["capitalize_first"], seed.category, ("capitalize_first",))
        upper = variant.upper()
        if upper != variant:
            yield Candidate(upper, seed.priority * 0.35, seed.category, ("uppercase",))


def generate_candidates(
    seeds: Iterable[NormalizedSeed],
    years: Iterable[str] = (),
    aggressive: bool = False,
    limit: int = 100_000,
) -> Iterator[Candidate]:
    """Stream candidates in human-probability order with global deduplication."""
    seen: set[str] = set()
    emitted = 0
    year_values = tuple(str(y) for y in years if y)

    def emit(candidate: Candidate) -> Iterator[Candidate]:
        nonlocal emitted
        if emitted >= limit or candidate.password in seen:
            return
        seen.add(candidate.password)
        emitted += 1
        yield candidate

    for seed in seeds:
        can_append_numeric = seed.classification not in {"numeric_suffix", "numeric", "mixed"}
        for base in _base_variants(seed):
            yield from emit(base)
            if emitted >= limit:
                return
            if can_append_numeric:
                for suffix in COMMON_SUFFIXES:
                    rule = "append_123" if suffix == "123" else "append_common_suffix"
                    yield from emit(Candidate(base.password + suffix, base.score * MUTATION_WEIGHTS.get(rule, 0.70), seed.category, base.rules + (rule,)))
                for year in year_values:
                    yield from emit(Candidate(base.password + year, base.score * MUTATION_WEIGHTS["append_year"], seed.category, base.rules + ("append_year",)))
            for leet, rule in _partial_leet(base.password):
                yield from emit(Candidate(leet, base.score * MUTATION_WEIGHTS["partial_leet"], seed.category, base.rules + (rule,)))
                if can_append_numeric:
                    for year in year_values[:2]:
                        yield from emit(Candidate(leet + year, base.score * 0.68, seed.category, base.rules + (rule, "append_year")))
            if aggressive:
                for prefix in COMMON_PREFIXES:
                    yield from emit(Candidate(prefix + base.password, base.score * MUTATION_WEIGHTS["prefix_symbol"], seed.category, base.rules + ("prefix_symbol",)))
                yield from emit(Candidate(f"xX_{base.password}_xX", base.score * MUTATION_WEIGHTS["edgy_wrap"], seed.category, base.rules + ("edgy_wrap",)))
