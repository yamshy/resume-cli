"""CLI entrypoint for resumecli Typer application."""

import typer


app = typer.Typer(name="resumecli")


@app.callback()
def main() -> None:
    """Root command callback placeholder."""


if __name__ == "__main__":
    app()

