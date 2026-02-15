# Schema Drift Detector - CLI

Schema Drift Detector is a CLI that: 
- Fetches a JSON payload from an HTTP API endpoint (GET for v1).
- Loads a “baseline” schema from a local file (JSON).
- Compares structure: added/removed/changed fields, type changes, optional vs required.
- Outputs the diff in three formats: JSON, Markdown, and a pretty terminal table.

## Language & Stack

I used Python and Click for the CLI as they make argument parsing, subcommands, and help text clean and maintainable.

## Output Examples

### JSON:
Simple: 
```bash 
print(json.dumps(diff, indent=2))
```
Good for machines and CI logs.

### Markdown:
```text
### Added fields

| Path              | Type   |
|-------------------|--------|
| `user.middle_name`| string |
```

### Pretty Terminal Table:
```text
ADDED | user.middle_name | - | string
```

## Installation

Use the package manager [pip](https://pypi.org/project/reorder-editable/) to install reorder-editable.

```bash
pip install -e .
```

## Usage

```bash
python -m schema_drift_cli --help
```

### Commands

- `version` - Shows the CLI version

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)

### Links

[PyPI](https://pypi.org/project/schema-drift-cli/)
