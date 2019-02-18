import click
import logging
import coloredlogs

from mutacc_auto import __version__
from .import_command import import_command

LOG_LEVELS = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
LOG = logging.getLogger(__name__)

@click.group()
@click.option('--loglevel', default='INFO', type=click.Choice(LOG_LEVELS))
@click.version_option(__version__)
@click.pass_context
def cli(context, loglevel):

    coloredlogs.install(level = loglevel)
    LOG.info("Running mutacc_auto")

cli.add_command(import_command)
