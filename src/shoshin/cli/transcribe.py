import click


@click.group()
def cli():
    pass


@cli.command()
def transcribe():
    click.echo("Transcribing...")


if __name__ == "__main__":
    cli()
