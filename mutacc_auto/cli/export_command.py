import click
import logging
from pathlib import Path

import yaml

from mutacc_auto.recipes.export_recipe import export_dataset
from mutacc_auto.utils.tmp_dir import TemporaryDirectory

MUTACC_TMP = 'temporaries'
MUTACC_ROOT_DIR = 'root_dir'

LOG = logging.getLogger(__name__)

def parse_path(ctx, param, value):

    if value:
        value = str(Path(str(value)).expanduser().absolute().resolve())
    return value

@click.command('export')
@click.option('-c', '--mutacc-config',
              type=click.Path(exists=True),
              callback=parse_path,
              help="configuration file used for mutacc")
@click.option('-o', '--vcf-out',
              type=click.Path(exists=False),
              callback=parse_path,
              help="Path to created vcf-file")
@click.option('-b', '--background',
              type=click.Path(exists=True),
              help="yaml file with genomic backgrounds for each sample in trio")
@click.option('-k', '--conda',
              is_flag=True,
              help="Use 'conda activate' to source environment")
@click.option('-e','--environment',
              type=str,
              help="conda environment used for mutacc")
@click.option('-D','--dry',
              is_flag=True,
              help="dry run")
@click.option('-V','--verbose',
              is_flag=True,
              help="verbose")
@click.pass_context
def export_command(ctx, mutacc_config, vcf_out, background, conda, environment, dry, verbose):

    mutacc_config = mutacc_config or ctx.obj['mutacc_config']
    mutacc_binary = ctx.obj.get('mutacc_binary')

    with open(background, 'r') as background_handle:
        background_datasets = yaml.load(background_handle)

    slurm_config = {}
    if ctx.obj.get('slurm'):
        slurm_config = ctx.obj['slurm']

    slurm_options = {}
    slurm_options['log_directory'] = slurm_config['log_directory']
    slurm_options['email'] = slurm_config['email']
    slurm_options['time'] = slurm_config['time']
    slurm_options['account'] = slurm_config['account']
    slurm_options['priority'] = slurm_config['priority']

    with open(Path(mutacc_config)) as yaml_handle:
        mutacc_config_dict = yaml.load(yaml_handle)
        mutacc_tmp = Path(mutacc_config_dict[MUTACC_ROOT_DIR]).joinpath(MUTACC_TMP)

    mutacc_auto_tmp_dir = mutacc_tmp.joinpath('mutacc_auto')
    if not mutacc_auto_tmp_dir.is_dir():
        mutacc_auto_tmp_dir.mkdir(parents=True)

    with TemporaryDirectory(directory=mutacc_auto_tmp_dir) as tmp_dir:

        LOG.info("All files are placed in {}".format(tmp_dir))
        sbatch_files = export_dataset(mutacc_config=mutacc_config,
                                      background=background_datasets,
                                      mutacc_binary=mutacc_binary,
                                      case_query='{}',
                                      merged_vcf_path=vcf_out,
                                      slurm_options=slurm_options,
                                      tmp_dir=tmp_dir,
                                      environment=environment,
                                      conda=conda,
                                      dry=dry)

    if verbose:

        for key, value in sbatch_files.items():

            with open(value) as sbatch_handle:

                LOG.info("SBATCH SCRIPT FOR {}, {}\n{}".format(key, value, sbatch_handle.read()))
