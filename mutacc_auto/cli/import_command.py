import click
import logging
from shutil import rmtree
from pathlib import Path
import yaml
import sys
import os

from mutacc_auto.recipes.import_recipe import import_extracted_case

LOG = logging.getLogger(__name__)

@click.command('import')
@click.option('-D','--dry',
              is_flag=True,
              help="dry run")
@click.pass_context
def import_command(ctx,
                   dry):

    import_dir = ctx.obj['import_dir']
    mutacc_config = ctx.obj['mutacc_config']
    mutacc_binary = ctx.obj['mutacc_binary']

    #For each case found in the import_dir stated in the mutacc config file
    #import to database
    for _, _, case_files in os.walk(import_dir):
        for filename in case_files:
            case_path = import_dir.joinpath(filename)

            ### IMPORT CASE AND DELETE FILE AFTERWARDS
            if str(case_path).endswith('mutacc.json'):
                LOG.info("importing {}".format(case_path))
                if not dry:
                    import_extracted_case(str(case_path), mutacc_config, mutacc_binary)
                    os.remove(case_path)
