import click
import logging
import coloredlogs
from pathlib import Path
import yaml

from mutacc_auto import __version__
from .extract_command import extract_command
from .import_command import import_command
from .export_command import export_command

MUTACC_IMPORT_DIR = 'imports'
MUTACC_TMP = 'temporaries'
MUTACC_ROOT_DIR = 'root_dir'

LOG_LEVELS = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
LOG = logging.getLogger(__name__)

def parse_path(ctx, param, value):

    if value:
        value = str(Path(str(value)).expanduser().absolute().resolve())
    return value

@click.group()
@click.option('--loglevel', default='INFO', type=click.Choice(LOG_LEVELS))
@click.option('--config-file', type=click.Path(exists=True), callback = parse_path)
@click.option('-L', '--log-directory',
    type=click.Path(exists=True),
    callback=parse_path,
    help="Directory for slurm logs")
@click.option('-E', '--email',
    type=str,
    help="email to notify")
@click.option('-t', '--time',
    type=str,
    help="Time for slurm jobs")
@click.option('-a', '--account',
    type=str,
    help="Account for slurm job")
@click.option('-P','--priority',
    type=str,
    help="priority for slurm job")
@click.version_option(__version__)
@click.pass_context
def cli(ctx, loglevel, config_file, log_directory, email, time, account, priority):

    coloredlogs.install(level = loglevel)
    LOG.info("Running mutacc_auto")

    config = {}
    if config_file:
        with open(config_file, 'r') as yaml_handle:
            config = yaml.load(yaml_handle, Loader=yaml.FullLoader)


    ctx.obj = {'mutacc_config': config['mutacc_config'],
               'mutacc_binary': config.get('mutacc_binary'),
               'mutacc_environment': config.get('mutacc_environment')}

    slurm_config = {}
    if config.get('slurm'):
        slurm_config = config['slurm']

    slurm_options = {}
    slurm_options['log_directory'] = log_directory or slurm_config['log_directory']
    slurm_options['email'] = email or slurm_config['email']
    slurm_options['time'] = time or slurm_config['time']
    slurm_options['account'] = account or slurm_config['account']
    slurm_options['priority'] = priority or slurm_config['priority']

    ctx.obj['slurm_options'] = slurm_options

    with open(Path(ctx.obj['mutacc_config'])) as yaml_handle:
        mutacc_config_dict = yaml.load(yaml_handle, Loader=yaml.FullLoader)
        mutacc_tmp = Path(mutacc_config_dict[MUTACC_ROOT_DIR]).joinpath(MUTACC_TMP)
        import_dir = Path(mutacc_config_dict[MUTACC_ROOT_DIR]).joinpath(MUTACC_IMPORT_DIR)

    mutacc_auto_tmp_dir = mutacc_tmp.joinpath('mutacc_auto')
    if not mutacc_auto_tmp_dir.is_dir():
        mutacc_auto_tmp_dir.mkdir(parents=True)

    ctx.obj['tmp_dir'] = mutacc_auto_tmp_dir
    ctx.obj['import_dir'] = import_dir


cli.add_command(extract_command)
cli.add_command(import_command)
cli.add_command(export_command)
