import typer

# The typer application object
app = typer.Typer(help="Schema Drift Detector CLI")

@app.callback(invoke_without_command=True)
def on_startup(ctx: typer.Context) -> None:
    """Schema Drift Detector CLI"""
    if ctx.invoked_subcommand is None:
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
    url: str = typer.Option(None, "--url", "-u", help="API URL to fetch baseline from"),
    file: str = typer.Option(None, "--file","-f",help="Local JSON file to use as baseline"),
    out: str = typer.Option("schema.json", "--out", "-o", help="Output schema file")
) -> None:
    """
    Initialize a baseline schema from an API URL or a local JSON file.
    """
    typer.echo("Initializing baseline schema...")
    typer.echo(f"Source: {url or file or 'none specified'}")
    typer.echo(f"Output: {out}")
    typer.echo("Done! (This is just a dummy version tho, real ones coming later)")

@app.command()
def check(
    url: str = typer.Option(None, "--url", "-u", help="API URL to check"),
    file: str = typer.Option(None, "--file","-f", help="Local JSON file to check"),
    schema: str = typer.Option("schema.json", "--schema", "-s", help="Baseline schema file"),
    output_format: str = typer.Option("table", "--output-format", "-of", help="Output format (json, markdown, table, all)"),
    fail_on_drift: bool = typer.Option(False, "--fail-on-drift", "-fod", help="Exit 1 if drift detected")
) -> None:
    """
    Check the current JSON against baseline schema.
    """
    typer.echo("Checking for schema drift...")
    typer.echo(f"Live Data: {url or file or 'none'}")
    typer.echo(f"Schema: {schema}")
    typer.echo(f"Format: {output_format}")
    typer.echo("No Drift Detected! (This is just a dummy version asw)")

    if fail_on_drift:
        typer.echo("    (fail-on-drift flag ignored for now)")

def main() -> None:
#     # Entrypoint that runs the Typer app
    app()


if __name__ == "__main__":
    # When I run this file directly with `python schema_drift_cli/cli.py`
    # Python sets __name__ to "__main__" and this block executes.
    main()