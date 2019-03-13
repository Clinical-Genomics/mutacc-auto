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

@click.command('import')
@click.option('-C','--config-file', type=click.Path(exists=True))
@click.option('-D','--dry', is_flag=True)
@click.option('-V','--verbose', is_flag=True)
@click.pass_context
def import_command(ctx,
                   config_file,
                   dry,
                   verbose):

    #Open and read config fore mutacc
    with open(Path(config_file)) as yaml_handle:

        mutacc_conf = yaml.load(yaml_handle)

    #Find directory where cases ready for import are stored
    import_dir = Path(mutacc_conf[MUTACC_ROOT_DIR]).joinpath(MUTACC_IMPORT_DIR)

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
