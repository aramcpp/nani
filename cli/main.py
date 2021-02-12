import typer


def main(host: str):
    typer.echo("nani - stress testing tool")
    typer.echo("use --help for more info")


if __name__ == "__main__":
    typer.run(main)