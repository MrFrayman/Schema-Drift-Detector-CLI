import json
from typing import Any

from rich.console import Console
from rich.table import Table

console = Console()


def render_json(diff: dict[str, Any]) -> str:
    return json.dumps(diff, indent=2, ensure_ascii=False)


def render_markdown(diff: dict[str, Any]) -> str:
    lines: list[str] = []

    def section(title: str, rows: list[dict[str, Any]], columns: list[str]) -> None:
        lines.append(f"### {title}")
        lines.append("")
        lines.append("| " + " | ".join(columns) + " |")
        lines.append("| " + " | ".join(["---"] * len(columns)) + " |")
        if not rows:
            lines.append("| (none) |")
            lines.append("")
            return
        for row in rows:
            values = [str(row.get(col.lower(), row.get(col, ""))) for col in columns]
            lines.append("| " + " | ".join(values) + " |")
        lines.append("")

    section("Added Fields", diff.get("added", []), ["Path", "Type"])
    section("Removed Fields", diff.get("removed", []), ["Path", "Type"])
    section("Changed Types", diff.get("changed_type", []), ["Path", "From", "To"])

    return "\n".join(lines).rstrip() + "\n"


def render_table(diff: dict[str, Any]) -> None:
    table = Table(title="Schema Drift")
    table.add_column("Change", style="cyan")
    table.add_column("Path", style="white")
    table.add_column("From", style="yellow")
    table.add_column("To", style="green")

    for row in diff.get("added", []):
        table.add_row("ADDED", row.get("path", ""), "-", row.get("type", ""))
    for row in diff.get("removed", []):
        table.add_row("REMOVED", row.get("path", ""), row.get("type", ""), "-")
    for row in diff.get("changed_type", []):
        table.add_row(
            "TYPE CHANGED", row.get("path", ""), row.get("from", ""), row.get("to", "")
        )

    console.print(table)
