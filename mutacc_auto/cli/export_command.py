import click
import logging
from pathlib import Path

import yaml

from mutacc_auto.recipes.export_recipe import export_dataset
from mutacc_auto.utils.tmp_dir import TemporaryDirectory

LOG = logging.getLogger(__name__)

def parse_path(ctx, param, value):

    if value:
        value = str(Path(str(value)).expanduser().absolute().resolve())
    return value

@click.command('export')
@click.option('-o', '--vcf-out',
              type=click.Path(exists=False),
              callback=parse_path,
              help="Path to created vcf-file")
@click.option('-b', '--background',
              type=click.Path(exists=True),
              callback=parse_path,
              help="yaml file with genomic backgrounds for each sample in trio")
@click.option('-d', '--dataset-dir',
              type=click.Path(exists=True),
              callback=parse_path,
              help="Directory where fastq files are placed")
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
def export_command(ctx, vcf_out, background, dataset_dir, conda, environment, dry, verbose):

    with open(background, 'r') as background_handle:
        background_datasets = yaml.load(background_handle, Loader=yaml.FullLoader)

    mutacc_config = ctx.obj['mutacc_config']
    mutacc_binary = ctx.obj.get('mutacc_binary')

    slurm_options = ctx.obj['slurm_options']

    mutacc_auto_tmp_dir = ctx.obj['tmp_dir']

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
                                      dry=dry,
                                      dataset_dir=dataset_dir)

    if verbose:

        for key, value in sbatch_files.items():

            with open(value) as sbatch_handle:

                LOG.info("SBATCH SCRIPT FOR {}, {}\n{}".format(key, value, sbatch_handle.read()))
