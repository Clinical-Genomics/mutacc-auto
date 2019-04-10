import logging

from mutacc_auto.commands.mutacc_command import MutAccExract
from mutacc_auto.commands.sbatch_command import SbatchCommand
from mutacc_auto.files.sbatch import SbatchScript

LOG = logging.getLogger(__name__)

def write_sbatch_script(tmp_dir,
                        environment,
                        mutacc_extract_command,
                        slurm_options,
                        log_directory,
                        email,
                        conda=False):

    """
        Function to write the sbatch script

        Args:
            tmp_dir (path): path to tmp dir where sbatch script is written
            environment (str): environment to run mutacc under
            mutacc_extract_command (str): mutacc command to extract reads
            log_directory (path): path to directory for log files
            email (str): email to notify if job failes/completes
            conda (bool): if True, activates environment with 'conda activate'

        Returns:
            sbatch_bath: path to sbatch script
    """

    with SbatchScript(
            tmp_dir,
            environment,
            slurm_options,
            log_directory,
            email=email,
            conda=conda
        ) as sbatch_handle:

        sbatch_handle.write_section(mutacc_extract_command)

        sbatch_path = sbatch_handle.path

    return sbatch_path



def get_mutacc_extract_command(mutacc_conf, input_file, padding, mutacc_binary=None):
    """
        Writes the mutacc command

        Args:
            mutacc_conf (path): path to mutacc config file
            input_file (path): path to case yaml file
            padding (int): padding

        Returns:
            mutacc_extract_command (str): mutacc command to be run for extraction
    """

    mutacc_extract_command = MutAccExract(mutacc_conf, padding, input_file, mutacc_binary=mutacc_binary)

    return str(mutacc_extract_command)

def sbatch_run(sbatch_script_path, dry=False):
    """
        Function to execute the sbatch script

        Args:
            sbatch_script_path (path): path to sbatch script
            wait (bool): if True, run sbatch with --wait flag
            dry (bool): if True, does not send job to slurm
    """
    sbatch_command = SbatchCommand(sbatch_script_path)

    if not dry:
        sbatch_command.call()
    else:
        LOG.info("Command; {}".format(sbatch_command))


def run_mutacc_extract(tmp_dir,
                       mutacc_config,
                       input_file,
                       padding,
                       environment,
                       slurm_options,
                       log_directory,
                       email,
                       conda=False,
                       wait=False,
                       dry=False,
                       mutacc_binary=None):

    """
        Function to extract reads from case


    """

    mutacc_extract_command = get_mutacc_extract_command(mutacc_config, input_file, padding, mutacc_binary=mutacc_binary)

    sbatch_script_path = write_sbatch_script(tmp_dir,
                                             environment,
                                             mutacc_extract_command,
                                             slurm_options,
                                             log_directory,
                                             email,
                                             conda)



    sbatch_run(sbatch_script_path, dry=dry)

    return sbatch_script_path
