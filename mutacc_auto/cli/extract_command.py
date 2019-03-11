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

LOG = logging.getLogger(__name__)

@click.command('extract')
@click.option('-c','--case-id', type=str)
@click.option('-d','--days-ago', type=int)
@click.option('-e','--environment', type=str)
@click.option('-C','--config-file', type=click.Path(exists=True))
@click.option('-L', '--log-directory', type=click.Path(exists=True))
@click.option('-E', '--email', type=str)
@click.option('-p','--padding', type=int)
@click.option('-D','--dry', is_flag=True)
@click.option('-V','--verbose', is_flag=True)
@click.option('-k', '--conda', is_flag=True)
@click.pass_context
def extract_command(ctx,
                    case_id,
                    days_ago,
                    environment,
                    config_file,
                    log_directory,
                    email,
                    padding,
                    dry,
                    verbose,
                    conda):

    #Open and read config fore mutacc
    with open(Path(config_file)) as yaml_handle:

        mutacc_conf = yaml.load(yaml_handle)

    #Find directory where cases ready for import are stored
    case_dir = Path(mutacc_conf['case_dir'])

    #Create a temporary dir to store created vcf, yaml, and script files
    with TemporaryDirectory() as tmp_dir:

        LOG.info("All files are placed in {}".format(tmp_dir))

        #Prepare input for case with case_id or days since updated
        inputs = get_inputs(tmp_dir, case_id=case_id, days_ago=days_ago, padding = padding)

        for case_input in inputs:
            #Extract reads for every case
            sbatch_script = run_mutacc_extract(
                    tmp_dir,
                    config_file,
                    case_input['input_file'],
                    case_input['padding'],
                    environment,
                    log_directory,
                    email=email,
                    conda=conda,
                    dry=dry
                )

            if verbose:

                with open(sbatch_script) as sbatch_handle:

                    LOG.info("\n{}".format(sbatch_handle.read()))
