import click
import logging
from shutil import rmtree
from pathlib import Path
import yaml
import sys
import os

from mutacc_auto.recipes.import_recipe import import_extracted_case

MUTACC_IMPORT_DIR = 'imports'
MUTACC_ROOT_DIR = 'root_dir'

LOG = logging.getLogger(__name__)

def parse_path(ctx, param, value):

    if value:
        value = str(Path(str(value)).expanduser().absolute().resolve())
    return value

@click.command('import')
@click.option('-D','--dry',
is_flag=True,
help="dry run")
@click.option('-V','--verbose',
is_flag=True,
help="verbose")
@click.pass_context
def import_command(ctx,
                   dry,
                   verbose):

    mutacc_config = ctx.obj['mutacc_config']
    #Open and read config for mutacc
    with open(Path(mutacc_config)) as yaml_handle:

        mutacc_config_dict = yaml.load(yaml_handle)

    #Find directory where cases ready for import are stored
    import_dir = Path(mutacc_config_dict[MUTACC_ROOT_DIR]).joinpath(MUTACC_IMPORT_DIR)

    #For each case found in the import_dir stated in the mutacc config file
    #import to database
    for _, _, case_files in os.walk(import_dir):
        for filename in case_files:
            case_path = import_dir.joinpath(filename)

            ### IMPORT CASE AND DELETE FILE AFTERWARDS
            if str(case_path).endswith('.mutacc'):
                LOG.info("importing {}".format(filename))
                if not dry:
                    import_extracted_case(str(case_path), config_file)
                    os.remove(case_path)
