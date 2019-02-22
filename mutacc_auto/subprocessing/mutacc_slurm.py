import subprocess
import tempfile
import logging
import datetime
import re

from mutacc_auto.utils import path_parse
from mutacc_auto.utils import sbatch_script


LOG = logging.getLogger(__name__)



def mutacc_slurm_extract(input_file, padding, environment, job_directory, mutacc_conf=None, sbatch_template=None):

    """
        Writes sbatch script and executes it

        Args:
            input_file(Path): path to input yaml file
            padding(int): bp to pad genomic region
            environment(str): Environmnet to use for mutacc
            job_directory(Path): directory to store sbatch script
            mutacc_conf(Path): configuration file for mutacc
            sbatch_template(Path): sbatch template
    """

    job_directory = path_parse.make_dir(job_directory)

    with sbatch_script.SbatchScript(
                                    sbatch_template,
                                    environment,
                                    job_directory,
                                    'mutacc_extract'
                                    ) as script_handle:

        script_handle.write_command("mutacc --config-file {} extract --padding {} --case {}".format(
                                        mutacc_conf,
                                        padding,
                                        input_file
            )
        )

        file_path = script_handle.path



    LOG.info("sbatch script: \n{}".format(
        subprocess.check_output(['cat', file_path]).decode("utf-8")
            )
        )

    #ADD SBATCH COMMAND WITH subprocess
    #USE --wait option so that script will continue only after
    #job is done

    try:

        subprocess.check_call(['sbatch', '--wait', file_path])

    except (OSError, subprocess.CalledProcessError):

        LOG.critical("Could not run command batch script")
