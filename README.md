# Schema-Drift-CLI

A small, pragmatic command-line tool to detect when an API's JSON response shape changes. Use it to compare a live response (or a local JSON sample) against a saved baseline schema and quickly surface added/removed fields, type changes, and flips between required/optional.

This project is intentionally lightweight — a local/CI guardrail rather than a full schema management platform.

---

## What it does

- Load JSON from a URL or a local file
- Infer a baseline schema from a JSON sample
- Compare a current JSON payload against the baseline
- Report:
  - added fields
  - removed fields
  - type changes (e.g., `string` → `number`)
  - changes in required vs optional
- Output results as JSON, Markdown, or a terminal table

Use this to catch breaking changes early or to make schema diffs easy to review.

---

## Quick Start

Install from PyPI and run one command:

```bash
pip install schema-drift-cli
schema-drift init --file sample.json --out schema.json
schema-drift check --schema schema.json --file sample_changed.json --output-format table
```

If you're working from the source tree during development, run the module directly:

```bash
python -m schema_drift_cli.cli check --schema schema.json --file sample_changed.json --output-format table
```

---

## Installation

From PyPI:
```bash
pip install schema-drift-cli
```

From source (development / latest):
```bash
git clone https://github.com/MrFrayman/Schema-Drift-Detector-CLI.git
cd Schema-Drift-Detector-CLI
pip install -e .
```

If the CLI binary doesn't behave like your working copy (common during development), either reinstall or run the module directly (example above).

---

## Commands & usage

Primary commands:

- `init` — infer a schema from a sample JSON file and save it
- `check` — compare a current JSON (file or HTTP response) against a saved baseline
- `version` — print the CLI version

Examples

Infer a baseline from a local file:
```bash
schema-drift init --file sample.json --out schema.json
# short flags: --file is -f, --out is -o
```

Compare a current JSON file against the baseline:
```bash
schema-drift check --schema schema.json --file sample_changed.json --output-format json
# output-format values: json | markdown | table
# short flags: --schema is -S, --file is -f, --output-format is -of
```

Show help:
```bash
schema-drift --help
schema-drift check --help
```

---

## Output formats

- `json` — machine-readable; ideal for CI or downstream tooling
- `markdown` — copy straight into PRs, changelogs, or docs
- `table` — quick human-readable terminal summary

Example JSON diff:
```json
{
  "added": [
    {"path": "user.middle_name", "type": "string"}
  ],
  "removed": [
    {"path": "user.age", "type": "number"}
  ],
  "changed": [
    {"path": "user.active", "old": "boolean", "new": "string"}
  ]
}
```

Example Markdown (useful for PR comments):
```markdown
### Added fields
| Path               | Type   |
|--------------------|--------|
| `user.middle_name` | string |

### Type changes
| Path          | Old     | New    |
|---------------|---------|--------|
| `user.active` | boolean | string |
```

Terminal table (quick local inspection):
```
ADDED   | user.middle_name | -       | string
REMOVED | user.age         | number  | -
CHANGED | user.active      | boolean | string
```

---

## Exit codes & CI integration

- `0` — no drift detected
- `1` — drift detected (suitable to fail a pipeline)
- `>1` — unexpected error (missing file, parse error, etc.)

Typical CI pattern:
1. Commit a known-good baseline (checked into the repo)
2. Run `schema-drift check` in your pipeline against the live API
3. Fail the build if the command exits with code `1`

---

## Limitations (current)

- GET / JSON only — no POST bodies or non-JSON formats supported
- No built-in auth flags (headers, tokens) yet — you can modify the code or use environment-level workarounds
- No schema versioning or historical timeline tracking
- No ignore rules or path-based filters yet

These are deliberate choices to keep the tool small and predictable. If you need richer behavior, consider contributing or extending the codebase.

---

## Tips & Troubleshooting

- Seeing "no such option: --output-format"? You may be calling an older installed `schema-drift` binary instead of your local working copy. Quick checks:
  - Run `schema-drift check --help` to inspect the installed binary's options.
  - Run the module directly during development:
    ```bash
    python -m schema_drift_cli.cli check --schema schema.json --file sample_changed.json --output-format json
    ```
  - Reinstall from your local source:
    ```bash
    pip install -e .
    ```

- If `render_table` doesn't print when using `--output-format table`, check whether the function returns a string or prints directly — the CLI expects a printable output for table mode.

- For authenticated endpoints, add a small wrapper script that injects headers or tokens into the response fetch step until native auth flags exist.

---

## Why Typer & Python

Typer provides a clean, Pythonic CLI with automatic help and helpful type signatures, keeping the code readable and maintainable. Python's batteries-included JSON handling and flexible data structures make schema inference and diffing straightforward, letting us keep the tool small and focused.

Yes, this could be implemented in Go or Node, but for quick iteration and developer ergonomics with JSON, Python is a pragmatic choice.

---

## Contributing

This repository is intentionally small and approachable. Open an issue if something surprises you or if you want a feature. PRs with tests and examples are especially appreciated.

Useful ideas right now:
- auth support (headers, tokens, OAuth)
- configurable ignore rules (paths, patterns)
- snapshot/monitor subcommand for scheduled checks
- richer diff output (context, sample values, fuzzy matching)

---

## License

MIT

Project page: https://pypi.org/project/schema-drift-cli/
