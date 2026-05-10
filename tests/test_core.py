from vaultforge.core.mutations.engine import generate_candidates
from vaultforge.core.scoring.engine import analyze_password
from vaultforge.core.seeds.engine import build_seeds
from vaultforge.core.simulation.engine import simulate_match
from vaultforge.core.ranking.engine import rank_candidates


def test_optional_fields_unicode_and_deduplication():
    seeds = build_seeds({"name": " Cárlos ", "team": "skip", "pet": "Luna", "anime": ""})
    variants = [variant for seed in seeds for variant in seed.variants()]
    assert "cárlos" in variants
    assert "carlos" in variants
    assert "luna" in variants
    assert all("none" not in variant for variant in variants)


def test_seed_contamination_avoids_double_numeric_suffix():
    seeds = build_seeds({"name": "Carlos123", "year": "2007"})
    candidates = list(generate_candidates(seeds, years=["2007"], limit=1000))
    assert all(candidate.password != "Carlos123123" for candidate in candidates)
    assert all(candidate.password != "carlos1232007" for candidate in candidates)


def test_false_complexity_is_detected():
    analysis = analyze_password("P@ssw0rd2025!")
    assert "false_complexity" in analysis.matched_patterns
    assert analysis.human_predictability == "HIGH"


def test_simulation_finds_human_mutation():
    seeds = build_seeds({"name": "Carlos", "year": "2007"})
    ranked = rank_candidates(generate_candidates(seeds, years=["2007"], limit=1000))
    result = simulate_match("Carlos2007", ranked)
    assert result.matched is True
    assert "append_year" in result.rule_matched
