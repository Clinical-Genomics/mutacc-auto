import click
import logging
from shutil import rmtree
import tempfile
from pathlib import Path

from mutacc_auto.build_input import input_assemble
from mutacc_auto.subprocessing import scout_call
from mutacc_auto.subprocessing.mutacc_slurm import mutacc_slurm_extract
from mutacc_auto.utils import path_parse

LOG = logging.getLogger(__name__)

@click.command('import')
@click.option('--case-id', type=str)
@click.option('--days-ago', type=int)
@click.option('--environment', type=str)
@click.option('--conf-file', type=click.Path(exists=True))
@click.option('--padding', type=int)
@click.pass_context
def import_command(ctx, case_id, days_ago, environment, conf_file, padding):
    """

    """
    #directory = path_parse.make_dir(temp_dir)
    tmp_dir = tempfile.mkdtemp(prefix='mutacc_auto_')
    tmp_dir = Path(tmp_dir)
    if case_id:
        cases = scout_call.find_cases(case_id)

    elif days_ago:
        cases = scout_call.find_cases_since(days=int(days_ago))

    else:
        LOG.critical("Please specify with option --case-id or --days-ago")

    inputs = []
    for case in cases:

        #Decide the padding
        #If the case is from WES, no padding will be added, else 300 bp
        if not padding:

            case_padding = 300
            for sample in case['individuals']:

                if sample['analysis_type'].upper() == 'WES':

                    case_padding = 0
        else:

            case_padding = padding

        inputs.append((input_assemble.assemble_case(case, tmp_dir), case_padding))

    for case_input in inputs:

        mutacc_slurm_extract(
            case_input[0],
            case_input[1],
            environment,
            tmp_dir,
            mutacc_conf=str(conf_file)
        )

    rmtree(tmp_dir)
