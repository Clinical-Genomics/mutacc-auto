import click
import logging
from pathlib import Path

from mutacc_auto.recipes.export_recipe import export_datasets

LOG = logging.getLogger(__name__)

def parse_path(ctx, param, value):

    if value:
        value = str(Path(str(value)).expanduser().absolute().resolve())
    return value

@click.command('export')
@click.option('-C','--mutacc-config',
    type=click.Path(exists=True),
    callback=parse_path,
    help="configuration file used for mutacc")
@click.option('-o','--vcf-out',
    type=click.Path(exists=False),
    callback=parse_path,
    help="Path to created vcf-file")
@click.pass_context
def export_command(ctx, mutacc_config, vcf_out):

    mutacc_config = mutacc_config or ctx.obj['mutacc_config']
    mutacc_binary = ctx.obj.get('mutacc_binary')

    files = export_datasets(mutacc_config=mutacc_config,
                            mutacc_binary=mutacc_binary,
                            case_query='{}',
                            merged_vcf_path=vcf_out)

    LOG.debug("files created: {}".format(files))
