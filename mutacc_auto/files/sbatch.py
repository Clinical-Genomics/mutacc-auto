
import datetime
import logging
from pathlib import Path
import tempfile


def get_timestamp():

    return str(datetime.datetime.now()).replace(' ','_').replace('.','_')

LOG = logging.getLogger(__name__)

SHEBANG = '#!/bin/bash'

HEADER_PREFIX = '#SBATCH'

JOBNAME = 'mutacc_' + get_timestamp()
ACCOUNT = 'prod001'
NODES = '1'
TIME = '4:00:00'
PRIORITY = 'low'
MAIL_FAIL = 'FAIL'
MAIL_END = 'END'

#SOME DEFAULT SBATCH OPTIONS
# (OPTION, VALUE)
HEADER_OPTIONS = (
    ('A', ACCOUNT),
    ('n', NODES),
    ('t', TIME),
    ('J', JOBNAME),
    ('qos', PRIORITY),
    ('mail-type', MAIL_FAIL),
    ('mail-type', MAIL_END)
)

ACTIVATE_ENVIRONMENT = "source activate"

STDERR_SUFFIX = "err"
STDOUT_SUFFIX = "out"

NEWLINE = "\n"

class SbatchScript():
    """
        Context manager to write sbatch scripts
    """

    @staticmethod
    def get_header(log_directory, email=None):

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
        #write all constant header options
        for option in HEADER_OPTIONS:
            if len(option[0]) == 1:
                header += f"{HEADER_PREFIX} -{option[0]} {option[1]}{NEWLINE}"
            else:
                header += f"{HEADER_PREFIX} --{option[0]}={option[1]}{NEWLINE}"

        #make log files
        log_directory = Path(log_directory)
        if not log_directory.is_dir():
            LOG.critical("No such directory: {}".format(log_directory))
            raise FileNotFoundError

        #Include Jobname in log file names
        stderr_file = log_directory.joinpath(f"{JOBNAME}.{STDERR_SUFFIX}")
        stdout_file = log_directory.joinpath(f"{JOBNAME}.{STDOUT_SUFFIX}")

        #write log files to header
        header += f"{HEADER_PREFIX} -e {stderr_file}{NEWLINE}"
        header += f"{HEADER_PREFIX} -o {stdout_file}{NEWLINE}"

        #If email is given, include this in header
        if email:
            header += f"{HEADER_PREFIX} --mail-user={email}{NEWLINE}"

        return header

    @staticmethod
    def get_environment(environment):

        """
            get command to run the correct environment
        """

        return f"{ACTIVATE_ENVIRONMENT} {environment}{NEWLINE}"

    @staticmethod
    def get_shebang():

        """
            Returns the shebang line
        """

        return SHEBANG


    def __init__(self, job_directory, environment, log_directory, email=None):

        """
            Args:
                job_directory (path): directory where sbatch script is written
                environment (str): environment to be used
                log_directory (path): path to dir for log files
                email (str): email to notify
        """

        self.script_handle = tempfile.NamedTemporaryFile(
                                        mode = 'w',
                                        dir = job_directory,
                                        delete = False
                                        )
        self.shebang = self.get_shebang()
        self.header = self.get_header(log_directory, email=email)
        self.environment = self.get_environment(environment)

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
