"""Streaming exporters to avoid materializing huge wordlists in RAM."""
from __future__ import annotations

import csv
import json
from collections.abc import Iterable
from pathlib import Path

from vaultforge.core.mutations.engine import Candidate


def export_candidates(candidates: Iterable[Candidate], output: Path, fmt: str = "txt") -> int:
    output.parent.mkdir(parents=True, exist_ok=True)
    count = 0
    with output.open("w", encoding="utf-8", newline="") as handle:
        if fmt == "json":
            handle.write("[\n")
            first = True
            for candidate in candidates:
                if not first:
                    handle.write(",\n")
                first = False
                handle.write(json.dumps(candidate.__dict__, ensure_ascii=False))
                count += 1
            handle.write("\n]\n")
        elif fmt == "csv":
            writer = csv.writer(handle)
            writer.writerow(["password", "score", "seed_category", "rules"])
            for candidate in candidates:
                writer.writerow([candidate.password, candidate.score, candidate.seed_category, ";".join(candidate.rules)])
                count += 1
        else:
            for candidate in candidates:
                handle.write(candidate.password + "\n")
                count += 1
    return count
