import click
import logging
from shutil import rmtree
from pathlib import Path
import yaml
import sys
import os
from pathlib import Path

from mutacc_auto.utils.tmp_dir import TemporaryDirectory
from mutacc_auto.recipes.input_recipe import get_inputs
from mutacc_auto.recipes.extract_recipe import run_mutacc_extract

LOG = logging.getLogger(__name__)


def parse_path(ctx, param, value):

    if value:
        value = str(Path(str(value)).expanduser().absolute().resolve())
    return value

@click.command('extract')
@click.option('-c','--case-id',
type=str,
help="case id used in scout and housekeeper")
@click.option('-d','--days-ago',
type=int,
help="days since last update of case")
@click.option('-e','--environment',
type=str,
help="conda environment used for mutacc"
)
@click.option('-C','--config-file',
type=click.Path(exists=True),
callback=parse_path,
help="configuration file used for mutacc"
)
@click.option('-L', '--log-directory',
type=click.Path(exists=True),
callback=parse_path,
help="Directory for slurm logs")
@click.option('-E', '--email',
type=str,
help="email to notify")
@click.option('-p','--padding',
type=int,
help="padding for genomic regions. this defaults to 0 for WES cases")
@click.option('-D','--dry',
is_flag=True,
help="dry run")
@click.option('-V','--verbose',
is_flag=True,
help="verbose")
@click.option('-k', '--conda',
is_flag=True,
help="Use 'conda activate' to source environment")
@click.option('--scout-config',
type=click.Path(exists=True),
callback=parse_path,
help="configuration file used for scout"
)
@click.option('--hk-config',
type=click.Path(exists=True),
callback=parse_path,
help="configuration file used for housekeeper"
)
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
                    conda,
                    scout_config,
                    hk_config):

    #Create a temporary dir to store created vcf, yaml, and script files
    with TemporaryDirectory() as tmp_dir:

        LOG.info("All files are placed in {}".format(tmp_dir))

        #Prepare input for case with case_id or days since updated
        inputs = get_inputs(tmp_dir, case_id=case_id, days_ago=days_ago,
                            padding = padding, scout_config=scout_config,
                            hk_config=hk_config)

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

                with open(case_input['input_file']) as input_handle:

                    LOG.info("\n{}".format(input_handle.read()))

                with open(sbatch_script) as sbatch_handle:

                    LOG.info("\n{}".format(sbatch_handle.read()))
