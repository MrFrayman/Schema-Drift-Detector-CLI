# Schema-Drift-CLI

A small, pragmatic tool to detect when an API's JSON response shape changes. It compares a live response (or a local JSON sample) against a saved baseline schema and reports added/removed fields, type changes, and required/optional shifts.

This is lightweight, meant to be a simple guardrail you can run locally or in CI, not a full-blown schema management system.

---

## What it does

- Load JSON from a URL or a local file
- Infer a baseline schema from a sample JSON
- Compare current JSON against the baseline
- Report:
  - added fields
  - removed fields
  - type changes (e.g., string → number)
  - changes in required vs optional
- Output as JSON, Markdown, or a terminal table

Useful for catching breaking changes early, and for making schema diffs easy to review.

---

## Installation

From PyPI:
```D:/My CodeDocs/CLI Projects/Schema-Drift-Detector-CLI/README.md#L251-260
pip install schema-drift-cli
```

From source (development / latest):
```D:/My CodeDocs/CLI Projects/Schema-Drift-Detector-CLI/README.md#L261-270
git clone https://github.com/MrFrayman/Schema-Drift-Detector-CLI.git
cd schema-drift-cli
pip install -e .
```

Note: if you edit the CLI code locally and the installed `schema-drift` command behaves differently, either reinstall or run the module directly (see Tips & Troubleshooting below).

---

## Commands & usage

This project exposes three primary commands that match the CLI in the repo:

- `init` — infer a schema from a sample JSON file and save it
- `check` — compare a current JSON (file or response) against a saved baseline
- `version` — print the CLI version

Basic usage examples:

Infer a baseline from a local file:
```D:/My CodeDocs/CLI Projects/Schema-Drift-Detector-CLI/README.md#L271-285
schema-drift init --file sample.json --out schema.json
# short flags: --file is -f, --out is -o
```

Compare a current JSON file against the baseline:
```D:/My CodeDocs/CLI Projects/Schema-Drift-Detector-CLI/README.md#L286-300
schema-drift check --schema schema.json --file sample_changed.json --output-format json
# output-format values: json | markdown | table
# short flags: --schema is -S, --file is -f, --output-format is -of
```

Show help for commands:
```D:/My CodeDocs/CLI Projects/Schema-Drift-Detector-CLI/README.md#L301-305
schema-drift --help
schema-drift check --help
```

If you want to run the exact code in your working tree (useful during development):
```D:/My CodeDocs/CLI Projects/Schema-Drift-Detector-CLI/README.md#L306-311
python -m schema_drift_cli.cli check --schema schema.json --file sample_changed.json --output-format table
```

---

## Output formats

- `json` — machine-readable; easy to use in CI or downstream tooling
- `markdown` — ready to paste into PRs, changelogs, or docs
- `table` — quick human-readable terminal summary

Example JSON diff:
```D:/My CodeDocs/CLI Projects/Schema-Drift-Detector-CLI/README.md#L312-330
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

Example Markdown (good for PR comments):
```D:/My CodeDocs/CLI Projects/Schema-Drift-Detector-CLI/README.md#L331-350
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
```D:/My CodeDocs/CLI Projects/Schema-Drift-Detector-CLI/README.md#L351-370
ADDED   | user.middle_name | -       | string
REMOVED | user.age         | number  | -
CHANGED | user.active      | boolean | string
```

---

## Exit codes & CI integration

- `0` — no drift detected
- `1` — drift detected (suitable to fail a pipeline)
- `>1` — unexpected error (missing file, parse error, etc.)

A typical CI pattern:
1. Save a known-good baseline (checked into the repo)
2. Run `schema-drift check` against the live API in your pipeline
3. Fail the build if the command exits with code `1`

---

## Limitations (current)

- GET / JSON only — no POST bodies or non-JSON formats supported
- No built-in auth flags (headers, tokens) yet — you can modify code or supply environment-level workarounds
- No schema versioning or historical timeline tracking
- No ignore rules or path-based filters yet

These are deliberate choices to keep the tool small and useful for quick checks. If you need more complex behaviors, consider contributing or extending the code.

---

## Tips & Troubleshooting

- If you see "no such option: --output-format" when running the CLI, it's often because the `schema-drift` command you're invoking is not the one from your working tree (for example, an older installed package). Quick checks:
  - Run `schema-drift check --help` to see the options the installed binary exposes.
  - Run the module directly during development:
    ```D:/My CodeDocs/CLI Projects/Schema-Drift-Detector-CLI/README.md#L371-375
    python -m schema_drift_cli.cli check --schema schema.json --file sample_changed.json --output-format json
    ```
  - Reinstall from your local source if needed:
    ```D:/My CodeDocs/CLI Projects/Schema-Drift-Detector-CLI/README.md#L376-380
    pip install -e .
    ```
- If `render_table` appears not to print when using `--output-format table`, check whether the function returns a string or prints directly — the CLI expects a printable output for table mode.

---

## Why Typer & Python

Typer gives a clean, Pythonic CLI with automatic help and argument parsing while keeping the code readable. Python's built-in JSON handling and data-structure ergonomics make it easy to implement schema inference and diffing without a lot of ceremony.

Yes, you could write this in Go or Node — but for quick iteration and tooling around JSON, Python is often the faster path.

---

## Contributing

This project is intentionally small and approachable. Help is welcome — open an issue if you hit a problem or want a feature. PRs with tests and examples are especially appreciated.

Ideas that are useful right now:
- auth support (headers, tokens, OAuth)
- configurable ignore rules (paths, patterns)
- snapshot/monitor subcommand for scheduled checks
- richer diff output (context, sample values, fuzzy matching)

---

## License

MIT

Project page: https://pypi.org/project/schema-drift-cli/
