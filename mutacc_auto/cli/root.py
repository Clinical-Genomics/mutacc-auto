import click
import logging
import coloredlogs
from pathlib import Path
import yaml

from mutacc_auto import __version__
from .extract_command import extract_command
from .import_command import import_command
from .export_command import export_command

LOG_LEVELS = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
LOG = logging.getLogger(__name__)

def parse_path(ctx, param, value):

    if value:
        value = str(Path(str(value)).expanduser().absolute().resolve())
    return value

@click.group()
@click.option('--loglevel', default='INFO', type=click.Choice(LOG_LEVELS))
@click.option('--config-file', type=click.Path(exists=True), callback = parse_path)
@click.version_option(__version__)
@click.pass_context
def cli(ctx, loglevel, config_file):

    coloredlogs.install(level = loglevel)
    LOG.info("Running mutacc_auto")

    config = {}
    if config_file:
        with open(config_file, 'r') as in_handle:
            config = yaml.load(in_handle)

    ctx.obj = config

cli.add_command(extract_command)
cli.add_command(import_command)
cli.add_command(export_command)
