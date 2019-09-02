import click
import logging
from shutil import rmtree
from pathlib import Path
import yaml
import sys
import os
from pathlib import Path
import json

from mutacc_auto.utils.tmp_dir import TemporaryDirectory
from mutacc_auto.procedures.input_procedure import get_input
from mutacc_auto.procedures.extract_procedure import run_mutacc_extract

LOG = logging.getLogger(__name__)

@click.command('extract')
@click.option('-c', '--case',
    type=str,
    help="JSON formated string containing case data (passed to mutacc-auto via cg)")
@click.option('-v', '--variants',
    type=str,
    help="JSON formated string containing variant data (passed to mutacc-auto via cg)")
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
                    case,
                    variants,
                    environment,
                    padding,
                    dry,
                    verbose,
                    conda):

    mutacc_config = ctx.obj['mutacc_config']
    mutacc_binary = ctx.obj.get('mutacc_binary')
    mutacc_environment = environment or ctx.obj.get('mutacc_environment')

    slurm_options = ctx.obj['slurm_options']

    mutacc_auto_tmp_dir = ctx.obj['tmp_dir']

    #Create a temporary dir to store created vcf, yaml, and script files
    with TemporaryDirectory(directory=mutacc_auto_tmp_dir) as tmp_dir:

        LOG.info("All files are placed in {}".format(tmp_dir))

        #Prepare input for case with case_id or days since updated
        input = get_input(tmp_dir,
                          case=json.loads(case),
                          variants=variants,
                          padding=padding)

        #Extract reads for every case
        sbatch_script = run_mutacc_extract(tmp_dir,
                                           mutacc_config,
                                           input['input_file'],
                                           input['padding'],
                                           input['case_id'],
                                           mutacc_environment,
                                           slurm_options,
                                           conda=conda,
                                           dry=dry,
                                           mutacc_binary=mutacc_binary)

        if verbose:

            with open(sbatch_script) as sbatch_handle:

                LOG.info("SBATCH SCRIPT {}\n{}".format(sbatch_script, sbatch_handle.read()))

            with open(input['input_file']) as input_handle:

                LOG.info("INPUT FILE {}\n{}".format(input['input_file'],input_handle.read()))


            with open(input['input_file']) as input_handle:
                input_file = yaml.load(input_handle, Loader=yaml.FullLoader)
            vcf_file = input_file['variants']

            with open(vcf_file) as vcf_handle:

                LOG.info("VCF FILE {}\n{}".format(vcf_file, vcf_handle.read()))
