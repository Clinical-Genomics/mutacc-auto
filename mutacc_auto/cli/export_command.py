import click
import logging
from pathlib import Path

import yaml

from mutacc_auto.recipes.export_recipe import export_dataset


LOG = logging.getLogger(__name__)

def parse_path(ctx, param, value):

    if value:
        value = str(Path(str(value)).expanduser().absolute().resolve())
    return value

@click.command('export')
@click.option('-C', '--mutacc-config',
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
@click.pass_context
def export_command(ctx, mutacc_config, vcf_out, background):

    mutacc_config = mutacc_config or ctx.obj['mutacc_config']
    mutacc_binary = ctx.obj.get('mutacc_binary')

    with open(background, 'r') as background_handle:
        background_datasets = yaml.load(background_handle)

    files = export_dataset(mutacc_config=mutacc_config,
                           background=background_datasets,
                           mutacc_binary=mutacc_binary,
                           case_query='{}',
                           merged_vcf_path=vcf_out)

    LOG.debug("files created: {}".format(files))
