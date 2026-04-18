import typer

from schema_drift_cli.diff import diff_schema
from schema_drift_cli.fetch import load_json_file, save_json_file
from schema_drift_cli.output import render_json, render_markdown, render_table
from schema_drift_cli.schema import infer_schema

# The typer application object
app = typer.Typer(help="Schema Drift Detector CLI")


@app.callback(invoke_without_command=True)
def main(ctx: typer.Context) -> None:
    """Schema Drift Detector CLI"""
    if ctx.invoked_subcommand is None:
        ascii_art = """
███████╗ ██████╗██╗  ██╗███████╗███╗   ███╗ █████╗     ██████╗ ██████╗ ██╗███████╗████████╗
██╔════╝██╔════╝██║  ██║██╔════╝████╗ ████║██╔══██╗    ██╔══██╗██╔══██╗██║██╔════╝╚══██╔══╝
███████╗██║     ███████║█████╗  ██╔████╔██║███████║    ██║  ██║██████╔╝██║█████╗     ██║
╚════██║██║     ██╔══██║██╔══╝  ██║╚██╔╝██║██╔══██║    ██║  ██║██╔══██╗██║██╔══╝     ██║
███████║╚██████╗██║  ██║███████╗██║ ╚═╝ ██║██║  ██║    ██████╔╝██║  ██║██║██║        ██║
╚══════╝ ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝     ╚═╝╚═╝  ╚═╝    ╚═════╝ ╚═╝  ╚═╝╚═╝╚═╝        ╚═╝

"""
        typer.echo(ascii_art)
        typer.echo("Welcome to the Schema Drift Detector CLI!")
        typer.echo("Use --help for more information")


@app.command()
def version() -> None:
    """
    Show the version of the schema-drift CLI
    """
    typer.echo("schema-drift version 0.1.0")


@app.command()
def init(
    file: str = typer.Option(
        ..., "--file", "-f", help="Local JSON file to use as the sample"
    ),
    out: str = typer.Option(
        "schema.json", "--out", "-o", help="Where to write the inferred schema"
    ),
) -> None:
    """Infer a baseline schema from a JSON file and save it."""
    data = load_json_file(file)
    schema = infer_schema(data)
    save_json_file(out, schema.to_dict())
    typer.echo(f"Saved inferred schema to {out}")


@app.command()
def check(
    schema: str = typer.Option(..., "--schema", "-S", help="Baseline schema file"),
    file: str = typer.Option(..., "--file", "-f", help="Current JSON file to compare"),
    output_format: str = typer.Option(
        "table", "--output-format", "-o", help="json, markdown, or table"
    ),
) -> None:
    """Compare a current JSON file against a saved baseline schema."""
    old_schema = load_json_file(schema)
    current_data = load_json_file(file)
    current_schema = infer_schema(current_data).to_dict()

    diff = diff_schema(old_schema, current_schema)
    result = diff.to_dict()

    if output_format == "json":
        typer.echo(render_json(result))
    elif output_format == "markdown":
        typer.echo(render_markdown(result))
    else:
        render_table(result)


def run() -> None:
    app()


if __name__ == "__main__":
    run()
