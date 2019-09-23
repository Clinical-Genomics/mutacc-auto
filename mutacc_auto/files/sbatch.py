
import datetime
import logging
from pathlib import Path
import tempfile

from mutacc_auto.files.constants import (
    SHEBANG,
    HEADER_PREFIX,
    JOBNAME,
    HEADER_OPTIONS,
    SOURCE_ACTIVATE,
    CONDA_ACTIVATE,
    STDERR_SUFFIX,
    STDOUT_SUFFIX,
    NEWLINE,
)

LOG = logging.getLogger(__name__)


class SbatchScript():
    """
        Context manager to write sbatch scripts
    """

    @staticmethod
    def get_header(slurm_options, job_prefix):

        """
            Returns header to be printed in sbatch scripts

            Args:
                log_directory (path): path to dir for log files
                email (str): email to notify if job fails, or completes

            Returns:
                header (str): string with header, lines separated by newline
        """

        #Instantiate header string
        header = ""

        #Find what options are given through command line
        cli_options = list(slurm_options.keys())
        #write all constant header options
        for key, value in HEADER_OPTIONS.items():

            #if option name not given through CLI, use dedault
            option_value = value[1]
            if key == 'jobname':
                option_value = f"{value[1]}_{job_prefix}"
            if key in cli_options:
                option_value = slurm_options[key]

            if len(value[0]) == 1:
                header += f"{HEADER_PREFIX} -{value[0]} {option_value}{NEWLINE}"
            else:
                header += f"{HEADER_PREFIX} --{value[0]}={option_value}{NEWLINE}"

        #make name of log files
        log_directory = Path(slurm_options['log_directory'])

        #Include Jobname in log file names
        stderr_file = log_directory.joinpath(f"{job_prefix}_{JOBNAME}.{STDERR_SUFFIX}")
        stdout_file = log_directory.joinpath(f"{job_prefix}_{JOBNAME}.{STDOUT_SUFFIX}")

        #write log files to header
        header += f"{HEADER_PREFIX} -e {stderr_file}{NEWLINE}"
        header += f"{HEADER_PREFIX} -o {stdout_file}{NEWLINE}"

        #If email is given, include this in header
        if slurm_options.get('email'):
            header += f"{HEADER_PREFIX} --mail-user={slurm_options['email']}{NEWLINE}"
            header += f"{HEADER_PREFIX} --mail-type=FAIL{NEWLINE}"
            header += f"{HEADER_PREFIX} --mail-type=END{NEWLINE}"
        return header

    @staticmethod
    def get_environment(environment, conda):

        """
            get command to run the correct environment
        """
        if conda:
            activate_command = CONDA_ACTIVATE
        else:
            activate_command = SOURCE_ACTIVATE

        return f"{activate_command} {environment}{NEWLINE}"

    @staticmethod
    def get_shebang():

        """
            Returns the shebang line
        """

        return SHEBANG


    def __init__(self, job_directory, environment, slurm_options, job_prefix="", conda=False):

        """
            Args:
                job_directory (path): directory where sbatch script is written
                environment (str): environment to be used
                log_directory (path): path to dir for log files
                email (str): email to notify
        """

        self.script_handle = tempfile.NamedTemporaryFile(suffix='.sh',
                                                         prefix='sbatch_',
                                                         mode='w',
                                                         dir=job_directory,
                                                         delete=False)
        self.shebang = self.get_shebang()
        self.header = self.get_header(slurm_options, job_prefix)
        self.environment = self.get_environment(environment, conda)

        #Write sections in script
        self.write_section(self.shebang)
        self.write_section(self.header)
        self.write_section(self.environment)

    def __enter__(self):

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):

        self.script_handle.close()

    def write_section(self, section):
        self.script_handle.write(f"{section}{NEWLINE}")


    @property
    def path(self):
        """
            Returns path to sbatch script
        """
        return self.script_handle.name
