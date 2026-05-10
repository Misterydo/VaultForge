"""VaultForge CLI."""
from __future__ import annotations

from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.table import Table

from vaultforge.core.config import MAX_PASSWORDS_HARD_LIMIT, clamp_limit
from vaultforge.core.exporters.stream import export_candidates
from vaultforge.core.mutations.engine import generate_candidates
from vaultforge.core.ranking.engine import rank_candidates
from vaultforge.core.scoring.engine import analyze_password
from vaultforge.core.seeds.engine import build_seeds
from vaultforge.core.simulation.engine import simulate_match

app = typer.Typer(help="VaultForge: Human Password Behavior Analysis Framework")
console = Console()

ETHICAL_NOTICE = """Ethical and Responsible Use: VaultForge is for personal auditing, research, education, and defensive security strengthening only. Unauthorized use against third parties is prohibited."""


def _input_map(**kwargs: Optional[str]) -> dict[str, Optional[str]]:
    return {key: value for key, value in kwargs.items()}


@app.callback()
def main() -> None:
    """Show the defensive-use warning for every command."""
    console.print(f"[yellow]{ETHICAL_NOTICE}[/yellow]")


@app.command()
def generate(
    name: Optional[str] = None,
    surname: Optional[str] = None,
    nickname: Optional[str] = None,
    year: Optional[str] = None,
    pet: Optional[str] = None,
    game: Optional[str] = None,
    team: Optional[str] = None,
    anime: Optional[str] = None,
    city: Optional[str] = None,
    limit: int = 100_000,
    aggressive: bool = False,
    output: Optional[Path] = None,
    format: str = typer.Option("txt", "--format", help="txt, json, or csv"),
    dry_run: bool = False,
) -> None:
    """Generate human-realistic password candidates from optional personal seeds."""
    safe_limit = clamp_limit(limit)
    seeds = build_seeds(_input_map(name=name, surname=surname, nickname=nickname, year=year, pet=pet, game=game, team=team, anime=anime, city=city))
    years = [seed.normalized for seed in seeds if seed.category == "year"]
    if dry_run:
        estimated = min(max(len(seeds), 1) * (40 if aggressive else 18), safe_limit)
        console.print(f"Estimated combinations: ~{estimated:,}")
        console.print("Estimated RAM: streaming output, low steady-state memory")
        console.print(f"Hard safety limit: {MAX_PASSWORDS_HARD_LIMIT:,}")
        return
    ranked = rank_candidates(generate_candidates(seeds, years=years, aggressive=aggressive, limit=safe_limit))
    if output:
        count = export_candidates(ranked, output, format)
        console.print(f"Exported {count:,} candidates to {output}")
        return
    for candidate in ranked[:safe_limit]:
        console.print(candidate.password)


@app.command()
def analyze(password: str, name: Optional[str] = None, year: Optional[str] = None) -> None:
    """Analyze perceived complexity versus real human predictability."""
    seeds = {seed.normalized for seed in build_seeds(_input_map(name=name, year=year))}
    result = analyze_password(password, seeds)
    table = Table(title=f"Password analyzed: {password}")
    table.add_column("Metric")
    table.add_column("Value")
    table.add_row("Entropy Score", f"{result.entropy} bits")
    table.add_row("Human Predictability", result.human_predictability)
    table.add_row("Perceived Strength", result.perceived_strength)
    table.add_row("Real Resistance", result.real_resistance)
    table.add_row("Matched Patterns", ", ".join(result.matched_patterns) or "none")
    for key, value in result.score_breakdown.items():
        table.add_row(key, value)
    console.print(table)


@app.command("testpwd")
def testpwd(password: str, name: Optional[str] = None, year: Optional[str] = None) -> None:
    """Alias for analyze, using the terminology from the project spec."""
    analyze(password, name, year)


@app.command()
def simulate(password: str, name: Optional[str] = None, year: Optional[str] = None, limit: int = 100_000) -> None:
    """Run a defensive local simulation over generated candidates."""
    seeds = build_seeds(_input_map(name=name, year=year))
    ranked = rank_candidates(generate_candidates(seeds, years=[year] if year else (), limit=clamp_limit(limit)))
    result = simulate_match(password, ranked)
    console.print("Simulation Results")
    console.print(f"Matched: {result.matched}")
    console.print(f"Attempts: {result.attempts:,}")
    console.print(f"Rule matched: {', '.join(result.rule_matched) or 'none'}")
    console.print(f"Estimated real-world resistance: {result.estimated_resistance}")


@app.command()
def entropy(password: str) -> None:
    """Print entropy-oriented analysis for a password."""
    result = analyze_password(password)
    console.print(f"Entropy: {result.entropy} bits")
    console.print(f"Human Predictability: {result.human_predictability}")

if __name__ == "__main__":
    app()
