# VaultForge

VaultForge is a **Human Password Behavior Analysis Framework**. It is not designed as “just another password cracker”; its core purpose is to model how humans create memorable passwords, then use that model for defensive analysis, education, and realistic resistance evaluation.

## Philosophy

Most users reuse patterns, mutate familiar words, add emotionally meaningful references, append dates, and rely on cognitive shortcuts. VaultForge focuses on those human behaviors instead of pure brute force.

## Core Pillars

| Pillar | Function |
| --- | --- |
| Generation Engine | Generate realistic human-style password candidates from optional seeds. |
| Analysis Engine | Evaluate entropy, human predictability, false complexity, and practical resistance. |

## Implemented Architecture

```text
vaultforge/
├── core/
│   ├── seeds/        # optional fields, normalization, Unicode + transliteration
│   ├── mutations/    # weighted human mutation chains
│   ├── ranking/      # probability-oriented ordering
│   ├── scoring/      # behavioral analysis and category scores
│   ├── entropy/      # mathematical entropy helpers
│   ├── simulation/   # defensive local match simulation
│   ├── rules/        # keyboard walks, suffixes, false complexity patterns
│   ├── datasets/     # separated built-in dataset categories
│   ├── exporters/    # streaming txt/json/csv exporters
│   └── utils/        # text normalization and seed classification
├── cli/              # Typer CLI
├── tui/              # Textual-ready TUI placeholder
├── configs/          # safe defaults
├── docs/             # ethics and project documentation
├── tests/            # pytest coverage
└── wordlists/        # local generated artifacts (empty by default)
```

## Safety and Ethics

VaultForge is for authorized defensive use only:

- personal password auditing;
- research;
- education;
- strengthening authentication security.

Unauthorized use against third parties is prohibited. The project does not support credential abuse, unauthorized access, intrusions, or illegal activity. Users are responsible for how they use the tool.

## Safe Defaults

- Default generation limit: `100,000` candidates.
- Hard generation limit: `1,000,000` candidates.
- Streaming exporters avoid holding huge wordlists in RAM.
- Optional fields ignore empty input plus explicit `none`, `null`, and `skip` values.
- Seed classification avoids contamination such as `Carlos123123`.

## CLI Examples

```bash
vaultforge generate --name Carlos --year 2007 --game Minecraft --limit 50000
vaultforge generate --name Carlos --year 2007 --pet Luna --output wordlists/demo.txt
vaultforge generate --name Carlos --year 2007 --dry-run
vaultforge analyze 'C@rlos2007!' --name Carlos --year 2007
vaultforge testpwd 'Carlos@2007' --name Carlos --year 2007
vaultforge simulate --password 'Carlos2007' --name Carlos --year 2007
vaultforge entropy 'P@ssw0rd2025!'
```

## Design Highlights

- **Optional fields are real optional fields:** missing anime, team, pet, nickname, or relationship values do not generate `None123` or empty seeds.
- **Unicode-aware normalization:** inputs are normalized while preserving Unicode and also generating ASCII-compatible variants, e.g. `joão` and `joao`.
- **Global deduplication:** candidate streams avoid duplicate output from overlapping rules.
- **Mutation chains:** common human order is prioritized, such as capitalization followed by year or suffix.
- **Partial leetspeak over total leetspeak:** realistic variants like `C@rlos2007` rank above edgy variants.
- **False complexity detection:** strings such as `P@ssw0rd!`, `Admin123`, and `Qwerty@2025` are flagged as predictable despite perceived strength.
- **Separated score categories:** reports distinguish entropy, human predictability, mutation resistance, and dictionary resistance.
- **English interface:** commands, help text, logs, configs, and docs are consistently English.

## Development

```bash
python -m pip install -e '.[test]'
pytest
```
