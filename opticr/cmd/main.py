#!/usr/bin/env python3
import click
from ant31box.cmd.default_config import default_config
from ant31box.cmd.version import version

from opticr.config import config

# from temporalloop.main import main as looper_main


@click.group()
@click.pass_context
def cli(ctx: click.Context) -> None:
    ctx.ensure_object(dict)


def main() -> None:
    # "init config"
    _ = config()
    # Start the Temporalio Worker
    #    cli.add_command(looper_main, name="looper")
    # start the FastAPI server
    # cli.add_command(server)
    # Display version
    cli.add_command(version)
    # Show default config
    cli.add_command(default_config)

    # Parse cmd-line arguments and options
    # pylint: disable=no-value-for-parameter
    cli()


if __name__ == "__main__":
    main()
