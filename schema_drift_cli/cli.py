import typer

# The typer application object
app = typer.Typer(help="Schema Drift Detector CLI")

@app.callback(invoke_without_command=True)
def main(ctx: typer.Context) -> None:
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


def main() -> None:
    # Entrypoint that runs the Typer app
    app()


if __name__ == "__main__":
    # When I run this file directly with `python schema_drift_cli/cli.py`
    # Python sets __name__ to "__main__" and this block executes.
    main()