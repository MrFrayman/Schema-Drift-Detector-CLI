# Schema-Drift-CLI

Detect when your API response structure changes. compares live endpoint against a baseline schema.

## What it does

- fetch JSON from an HTTP endpoint
- compare it against a saved baseline schema
- show what changed: added fields, removed fields, type changes, required vs optional
- output the diff as JSON, markdown, or a terminal table

useful for catching breaking changes before they break your app.

## How it works

```bash
# compare live API against baseline
schema-drift check https://api.example.com/users baseline.json

# outputs show you exactly what drifted
```

handles:
- nested objects
- arrays
- type changes (string → number, etc)
- optional/required field shifts

doesn't handle:
- POST/PUT endpoints (v1 is GET only)
- authentication (yet)
- schema versioning
- historical drift tracking

## Output formats

### JSON
machine-readable. good for CI pipelines or piping to other tools.

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

### Markdown
works in docs, PRs, or anywhere you need readable tables.

```markdown
### Added fields
| Path              | Type   |
|-------------------|--------|
| `user.middle_name`| string |

### Type changes
| Path         | Old     | New    |
|--------------|---------|--------|
| `user.active`| boolean | string |
```

### Terminal Table
quick visual scan when you just run it locally.

```
ADDED   | user.middle_name | -       | string
REMOVED | user.age        | number  | -
CHANGED | user.active     | boolean | string
```

## Installation

```bash
pip install schema-drift-cli
```

or install from source:

```bash
git clone https://github.com/yourusername/schema-drift-cli
cd schema-drift-cli
pip install -e .
```

## Usage

```bash
# check drift
schema-drift check <endpoint-url> <baseline-file> [--format json|markdown|table]

# save current response as baseline
schema-drift snapshot <endpoint-url> <output-file>

# show version
schema-drift version
```

### Creating a baseline

first time setup:

```bash
# grab current schema as your baseline
schema-drift snapshot https://api.example.com/users baseline.json
```

then later:

```bash
# check if anything changed
schema-drift check https://api.example.com/users baseline.json
```

exits with code 0 if no drift, 1 if drift detected. good for CI gates.

## Why python + click

click makes CLI parsing clean. you get help text, subcommands, and validation without much code. python's `requests` + `json` libs handle the HTTP and comparison logic simply.

could've done it in node or go, but for a schema diff tool, python's data handling is straightforward.

## Limitations

- GET requests only right now
- no auth headers (you can add them in code, but not via CLI flags yet)
- doesn't track when drift happened, just that it did
- assumes JSON responses (no XML, no protobuf)

if your endpoint needs auth or uses POST, you'll need to modify the source or wait for v2.

## Contributing

if you hit bugs or want features, open an issue. PRs welcome, especially for:
- auth support (headers, tokens)
- better diff algorithms
- ignoring certain paths
- config file support

## License

MIT

[pypi](https://pypi.org/project/schema-drift-cli/)
