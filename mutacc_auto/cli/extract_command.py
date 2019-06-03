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

@click.command('extract')
@click.option('-c','--case-id',
    type=str,
    help="case id used in scout and housekeeper")
@click.option('-d','--days-ago',
    type=int,
    help="days since last update of case")
@click.option('-e','--environment',
    type=str,
    help="conda environment used for mutacc")
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
@click.pass_context
def extract_command(ctx,
                    case_id,
                    days_ago,
                    environment,
                    padding,
                    dry,
                    verbose,
                    conda):

    scout_config = ctx.obj.get('scout_config')
    scout_binary = ctx.obj.get('scout_binary')
    hk_config = ctx.obj.get('hk_config')
    hk_binary = ctx.obj.get('hk_binary')
    mutacc_config = ctx.obj['mutacc_config']
    mutacc_binary = ctx.obj.get('mutacc_binary')

    slurm_options = ctx.obj['slurm_options']

    mutacc_auto_tmp_dir = ctx.obj['tmp_dir']

    #Create a temporary dir to store created vcf, yaml, and script files
    with TemporaryDirectory(directory=mutacc_auto_tmp_dir) as tmp_dir:

        LOG.info("All files are placed in {}".format(tmp_dir))

        #Prepare input for case with case_id or days since updated
        inputs = get_inputs(tmp_dir, case_id=case_id, days_ago=days_ago,
                            padding=padding, scout_config=scout_config,
                            scout_binary=scout_binary, hk_config=hk_config,
                            hk_binary=hk_binary)

        for case_input in inputs:
            #Extract reads for every case
            sbatch_script = run_mutacc_extract(tmp_dir,
                                               mutacc_config,
                                               case_input['input_file'],
                                               case_input['padding'],
                                               case_input['case_id'],
                                               environment,
                                               slurm_options,
                                               conda=conda,
                                               dry=dry,
                                               mutacc_binary=mutacc_binary)

            if verbose:

                with open(sbatch_script) as sbatch_handle:

                    LOG.info("SBATCH SCRIPT {}\n{}".format(sbatch_script, sbatch_handle.read()))

                with open(case_input['input_file']) as input_handle:

                    LOG.info("INPUT FILE {}\n{}".format(case_input['input_file'],input_handle.read()))


                with open(case_input['input_file']) as input_handle:
                    input_file = yaml.load(input_handle, Loader=yaml.FullLoader)
                vcf_file = input_file['variants']

                with open(vcf_file) as vcf_handle:

                    LOG.info("VCF FILE {}\n{}".format(vcf_file, vcf_handle.read()))
