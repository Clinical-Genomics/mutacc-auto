import click
import logging
from shutil import rmtree
from pathlib import Path
import yaml
import sys
import os

from mutacc_auto.utils.tmp_dir import TemporaryDirectory
from mutacc_auto.recipes.input_recipe import get_inputs
from mutacc_auto.recipes.extract_recipe import run_mutacc_extract
from mutacc_auto.recipes.import_recipe import import_extracted_case

LOG = logging.getLogger(__name__)

@click.command('import')
@click.option('--case-id', type=str)
@click.option('--days-ago', type=int)
@click.option('--environment', type=str)
@click.option('--conf-file', type=click.Path(exists=True))
@click.option('--padding', type=int)
@click.option('--dry', is_flag=True)
@click.pass_context
def import_command(ctx, case_id, days_ago, environment, conf_file, padding, dry):

    #Open and read config fore mutacc
    with open(Path(conf_file)) as yaml_handle:

        mutacc_conf = yaml.load(yaml_handle)

    #Find directory where cases ready for import are stored
    case_dir = Path(mutacc_conf['case_dir'])

    #Create a temporary dir to store created vcf, yaml, and script files
    with TemporaryDirectory() as tmp_dir:

        #Prepare input for case with case_id or days since updated
        inputs = get_inputs(tmp_dir, case_id=case_id, days_ago=days_ago, padding = padding)

        for case_input in inputs:
            #Extract reads for every case
            run_mutacc_extract(
                tmp_dir,
                conf_file,
                case_input['input_file'],
                case_input['padding'],
                environment,
                stdout_file='STDOUT.txt',
                stderr_file='STDERR.txt',
                email='EMAIL@...',
                wait=True,
                dry=dry
            )

    #For each case found in the case_dir stated in the mutacc config file
    #import to database
    for _, _, case_files in os.walk(case_dir):
        for filename in case_files:
            case_path = case_dir.joinpath(filename)
            LOG.info("importing {}".format(filename))

            ### IMPORT CASE AND DELETE FILE AFTERWARDS
            if str(case_path).endswith('.mutacc'):
                import_extracted_case(str(case_path), conf_file)
                os.remove(case_path)
